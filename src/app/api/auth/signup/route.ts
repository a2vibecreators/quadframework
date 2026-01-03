/**
 * POST /api/auth/signup
 *
 * Create new organization and user account.
 * Supports both passwordless (startup/business) and password-based (legacy) signup.
 *
 * Passwordless flow (orgType = startup | business):
 * 1. Create org and user (no password)
 * 2. Send OTP/magic link to email
 * 3. User verifies via /api/auth/verify-code
 *
 * Password flow (legacy or orgType = null):
 * 1. Create org and user with password
 * 2. Return token directly
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import crypto from 'crypto';

// Generate a random password for passwordless accounts (they'll never use it)
function generateRandomPassword(): string {
  return crypto.randomBytes(32).toString('hex');
}

// Generate 6-digit OTP
function generateOTP(): string {
  return Math.floor(100000 + Math.random() * 900000).toString();
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, fullName, companyName, orgType, password } = body;

    // Validation
    if (!email) {
      return NextResponse.json(
        { error: 'Email is required' },
        { status: 400 }
      );
    }

    // Normalize email
    const normalizedEmail = email.toLowerCase().trim();

    // Check if email already exists
    const existingUser = await prisma.qUAD_users.findUnique({
      where: { email: normalizedEmail },
    });

    if (existingUser) {
      return NextResponse.json(
        { error: 'An account with this email already exists. Please sign in instead.' },
        { status: 409 }
      );
    }

    // Determine signup type
    const isPasswordless = orgType === 'startup' || orgType === 'business';
    const finalPassword = isPasswordless ? generateRandomPassword() : password;

    if (!isPasswordless && !password) {
      return NextResponse.json(
        { error: 'Password is required for this signup type' },
        { status: 400 }
      );
    }

    // Determine company name
    const finalCompanyName = companyName || `${fullName || 'User'}'s Team`;

    // Map orgType to size for database
    const sizeMap: Record<string, string> = {
      startup: 'startup',
      business: 'medium',
      enterprise: 'enterprise',
    };
    const orgSize = sizeMap[orgType as string] || 'medium';

    // Create organization (tier_id will be set during setup)
    const organization = await prisma.qUAD_organizations.create({
      data: {
        name: finalCompanyName,
        admin_email: normalizedEmail,
        size: orgSize,
        is_active: true,
      },
    });

    // Hash password (even for passwordless - it's a random string)
    const bcrypt = await import('bcryptjs');
    const passwordHash = await bcrypt.hash(finalPassword, 10);

    // Create user as OWNER
    const user = await prisma.qUAD_users.create({
      data: {
        org_id: organization.id,
        email: normalizedEmail,
        password_hash: passwordHash,
        role: 'OWNER',
        full_name: fullName || 'User',
        is_active: true,
        email_verified: false, // Will be verified via OTP
      },
    });

    // Create org setup status
    await prisma.qUAD_org_setup_status.create({
      data: {
        org_id: organization.id,
        meeting_provider_configured: false,
        calendar_connected: false,
        ai_tier_selected: false,
        first_domain_created: false,
        first_circle_created: false,
        git_provider_connected: false,
      },
    });

    // For passwordless signup, generate and store OTP
    if (isPasswordless) {
      const otp = generateOTP();
      const expiresAt = new Date(Date.now() + 10 * 60 * 1000); // 10 minutes

      // Delete any existing codes for this email
      await prisma.qUAD_email_verification_codes.deleteMany({
        where: { email: normalizedEmail },
      });

      // Create new verification code
      await prisma.qUAD_email_verification_codes.create({
        data: {
          email: normalizedEmail,
          code: otp,
          expires_at: expiresAt,
          attempts: 0,
          used: false,
        },
      });

      // In production, send email here
      // For now, log OTP (dev mode)
      console.log(`[DEV] Signup OTP for ${normalizedEmail}: ${otp}`);

      return NextResponse.json({
        success: true,
        message: 'Account created. Please check your email for the verification code.',
        autoLogin: false,
        requiresVerification: true,
        email: normalizedEmail,
        // DEV ONLY - remove in production
        ...(process.env.NODE_ENV === 'development' && { devOtp: otp }),
      });
    }

    // Password-based signup - return token directly (legacy flow)
    const { generateToken, createSession } = await import('@/lib/auth');

    const token = generateToken({
      id: user.id,
      org_id: organization.id,
      email: user.email,
      role: user.role,
      full_name: user.full_name || '',
      is_active: user.is_active,
    });

    const ipAddress = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || null;
    const userAgent = request.headers.get('user-agent') || null;
    await createSession(user.id, token, ipAddress, userAgent);

    // Mark email as verified for password signups
    await prisma.qUAD_users.update({
      where: { id: user.id },
      data: { email_verified: true },
    });

    return NextResponse.json({
      success: true,
      message: 'Account created successfully',
      autoLogin: true,
      data: {
        organization: {
          id: organization.id,
          name: organization.name,
        },
        user: {
          id: user.id,
          email: user.email,
          role: user.role,
          fullName: user.full_name,
        },
        token,
      },
    }, { status: 201 });

  } catch (error) {
    console.error('Signup error:', error);
    return NextResponse.json(
      { error: 'Failed to create account. Please try again.' },
      { status: 500 }
    );
  }
}
