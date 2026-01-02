/**
 * GET /api/skills - Get user skills
 * POST /api/skills - Add new skill
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifyToken } from '@/lib/auth';

// GET: Get skills
export async function GET(request: NextRequest) {
  try {
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const token = authHeader.substring(7);
    const payload = verifyToken(token);
    if (!payload) {
      return NextResponse.json({ error: 'Invalid token' }, { status: 401 });
    }

    const { searchParams } = new URL(request.url);
    const userId = searchParams.get('user_id') || payload.userId;
    const view = searchParams.get('view') || 'user'; // user, org, categories

    if (view === 'org') {
      // Get all skills in organization with counts
      const skills = await prisma.qUAD_user_skills.groupBy({
        by: ['skill_name', 'skill_category'],
        where: { org_id: payload.companyId },
        _count: { id: true },
        _avg: { proficiency_level: true }
      });

      const organized = skills.reduce((acc, s) => {
        const category = s.skill_category || 'uncategorized';
        if (!acc[category]) acc[category] = [];
        acc[category].push({
          name: s.skill_name,
          user_count: s._count.id,
          avg_proficiency: Math.round((s._avg.proficiency_level || 0) * 10) / 10
        });
        return acc;
      }, {} as Record<string, Array<{ name: string; user_count: number; avg_proficiency: number }>>);

      return NextResponse.json({ skills_by_category: organized });
    }

    if (view === 'categories') {
      // Return skill category definitions
      const categories = [
        { id: 'technical', name: 'Technical', examples: ['JavaScript', 'Python', 'AWS', 'Docker'] },
        { id: 'soft', name: 'Soft Skills', examples: ['Communication', 'Leadership', 'Problem Solving'] },
        { id: 'domain', name: 'Domain', examples: ['Healthcare', 'Finance', 'E-commerce'] },
        { id: 'ai', name: 'AI & ML', examples: ['Prompt Engineering', 'RAG', 'Fine-tuning'] },
        { id: 'tool', name: 'Tools', examples: ['Jira', 'Figma', 'VS Code', 'GitHub'] }
      ];
      return NextResponse.json({ categories });
    }

    // Get user's skills
    const skills = await prisma.qUAD_user_skills.findMany({
      where: { user_id: userId, org_id: payload.companyId },
      orderBy: [{ skill_category: 'asc' }, { proficiency_level: 'desc' }]
    });

    // Group by category
    const skillsByCategory = skills.reduce((acc, s) => {
      const category = s.skill_category || 'uncategorized';
      if (!acc[category]) acc[category] = [];
      acc[category].push(s);
      return acc;
    }, {} as Record<string, typeof skills>);

    // Calculate stats
    const totalSkills = skills.length;
    const certifiedSkills = skills.filter(s => s.certified).length;
    const avgProficiency = skills.length > 0
      ? Math.round(skills.reduce((sum, s) => sum + s.proficiency_level, 0) / skills.length * 10) / 10
      : 0;

    return NextResponse.json({
      user_id: userId,
      skills,
      skills_by_category: skillsByCategory,
      stats: {
        total_skills: totalSkills,
        certified_skills: certifiedSkills,
        avg_proficiency: avgProficiency
      }
    });

  } catch (error) {
    console.error('Get skills error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

// POST: Add skill
export async function POST(request: NextRequest) {
  try {
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const token = authHeader.substring(7);
    const payload = verifyToken(token);
    if (!payload) {
      return NextResponse.json({ error: 'Invalid token' }, { status: 401 });
    }

    const body = await request.json();
    const { skill_name, skill_category, proficiency_level, certified, certification_date } = body;

    if (!skill_name) {
      return NextResponse.json({ error: 'skill_name is required' }, { status: 400 });
    }

    // Validate proficiency level
    const level = proficiency_level || 1;
    if (level < 1 || level > 5) {
      return NextResponse.json(
        { error: 'proficiency_level must be between 1 and 5' },
        { status: 400 }
      );
    }

    // Upsert skill (update if exists)
    const skill = await prisma.qUAD_user_skills.upsert({
      where: {
        user_id_skill_name: {
          user_id: payload.userId,
          skill_name
        }
      },
      update: {
        skill_category,
        proficiency_level: level,
        certified: certified || false,
        certification_date: certification_date ? new Date(certification_date) : null
      },
      create: {
        user_id: payload.userId,
        org_id: payload.companyId,
        skill_name,
        skill_category,
        proficiency_level: level,
        certified: certified || false,
        certification_date: certification_date ? new Date(certification_date) : null
      }
    });

    return NextResponse.json({ skill }, { status: 201 });

  } catch (error) {
    console.error('Create skill error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
