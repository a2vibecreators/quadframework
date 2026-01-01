'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useSession } from 'next-auth/react';
import PageNavigation from '@/components/PageNavigation';

// Book chapters data
const chapters = [
  {
    number: 1,
    title: 'The AI Paradox',
    description: 'Java-specific disaster stories - NullPointerException, memory leaks, thread safety issues AI ignores.',
    preview: 'AI can write Java code faster than any human. But speed without understanding is a recipe for disaster...',
    readTime: '15 min',
  },
  {
    number: 2,
    title: 'Java Types',
    description: 'Primitives vs wrappers, autoboxing pitfalls, BigDecimal for money, String immutability.',
    preview: 'The difference between int and Integer seems trivial until AI generates code that crashes in production...',
    readTime: '20 min',
  },
  {
    number: 3,
    title: 'Control Flow',
    description: 'If/switch, loops, AND when to use streams - AI generating loops when streams are cleaner.',
    preview: 'Traditional loops have their place, but AI often misses when a stream would be more elegant...',
    readTime: '18 min',
  },
  {
    number: 4,
    title: 'OOP Foundations',
    description: 'Classes, objects, constructors, this, static - AI creating unnecessary objects or wrong static usage.',
    preview: 'Object-oriented programming is Java\'s core paradigm, but AI frequently misunderstands the fundamentals...',
    readTime: '22 min',
  },
  {
    number: 5,
    title: 'OOP Pillars',
    description: 'Encapsulation, inheritance, polymorphism, abstraction - AI making everything public.',
    preview: 'The four pillars of OOP are where AI makes its most dangerous mistakes...',
    readTime: '25 min',
  },
  {
    number: 6,
    title: 'Error Handling',
    description: 'Exception hierarchy, checked vs unchecked, try-with-resources, AI swallowing exceptions.',
    preview: 'Java\'s exception system is rich and nuanced. AI often oversimplifies to the point of danger...',
    readTime: '20 min',
  },
  {
    number: 7,
    title: 'Collections',
    description: 'ArrayList vs LinkedList, HashMap vs TreeMap - AI using wrong collection types.',
    preview: 'Choosing the right collection is crucial for performance. AI rarely makes the optimal choice...',
    readTime: '22 min',
  },
  {
    number: 8,
    title: 'Modern Java',
    description: 'Streams, lambdas, Optional, functional interfaces - when AI overuses or underuses modern features.',
    preview: 'Modern Java features are powerful but AI often applies them inappropriately...',
    readTime: '25 min',
  },
  {
    number: 9,
    title: 'Prompting AI for Java',
    description: 'Specifying Java version, mentioning existing classes, requesting specific implementations.',
    preview: 'How you prompt AI determines the quality of Java code you get. Learn the techniques...',
    readTime: '18 min',
  },
  {
    number: 10,
    title: 'Reviewing Java Output',
    description: 'Raw types, missing null checks, wrong collections, ignoring class hierarchy.',
    preview: 'A checklist for catching AI\'s most common Java mistakes before they hit production...',
    readTime: '20 min',
  },
  {
    number: 11,
    title: 'The QUAD Framework',
    description: 'Q-U-A-D stages, AI Adoption Matrix, Role-stage participation, The 4 Circles.',
    preview: 'How teams organize around AI with QUAD - from stages to circles to the adoption matrix...',
    readTime: '30 min',
    badge: 'NEW',
  },
  {
    number: 12,
    title: 'Practical QUAD Workflows',
    description: 'Brand new laptop setup to production - real workflows using QUAD principles.',
    preview: 'From your first day to production incidents - practical workflows for the AI era...',
    readTime: '35 min',
    badge: 'NEW',
  },
];

export default function BookPage() {
  const { data: session, status } = useSession();
  const [downloading, setDownloading] = useState(false);
  const [downloadSuccess, setDownloadSuccess] = useState(false);
  const [expandedChapter, setExpandedChapter] = useState<number | null>(null);

  const handleDownload = async () => {
    if (!session) {
      // Redirect to login
      window.location.href = '/auth/login?callbackUrl=/book';
      return;
    }

    setDownloading(true);
    try {
      const response = await fetch('/api/book/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'Java-for-the-AI-Era-QUAD.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        setDownloadSuccess(true);
      } else {
        throw new Error('Download failed');
      }
    } catch (error) {
      console.error('Download error:', error);
      alert('Download failed. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <PageNavigation />

      {/* Hero Section */}
      <section className="relative py-16 px-8 overflow-hidden">
        {/* Background decoration */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
        </div>

        <div className="max-w-6xl mx-auto relative">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Book Cover */}
            <div className="flex justify-center">
              <div className="relative group">
                {/* Book shadow */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg transform rotate-3 group-hover:rotate-6 transition-transform"></div>
                {/* Book */}
                <div className="relative bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg p-8 border border-slate-700 shadow-2xl transform group-hover:-rotate-1 transition-transform">
                  <div className="w-64 h-80 flex flex-col justify-between">
                    {/* Top */}
                    <div>
                      <div className="text-xs text-blue-400 font-mono mb-2">A2VIBE CREATORS</div>
                      <div className="text-4xl font-black mb-2">
                        <span className="text-blue-400">Java</span>
                      </div>
                      <div className="text-lg text-slate-300 mb-2">for the</div>
                      <div className="text-3xl font-black bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
                        AI Era
                      </div>
                    </div>
                    {/* Middle */}
                    <div className="flex items-center gap-4 py-6">
                      <div className="text-6xl">☕</div>
                      <div className="text-4xl">+</div>
                      <div className="text-6xl">🤖</div>
                    </div>
                    {/* Bottom */}
                    <div>
                      <div className="text-sm text-slate-400 mb-1">Includes QUAD Framework</div>
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 rounded text-xs">v3.0</span>
                        <span className="px-2 py-0.5 bg-green-500/20 text-green-300 rounded text-xs">12 Chapters</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Book Info */}
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm font-medium mb-4">
                <span>📖</span>
                <span>FREE for registered users</span>
              </div>

              <h1 className="text-4xl md:text-5xl font-black mb-4">
                Java for the <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">AI Era</span>
              </h1>

              <p className="text-xl text-slate-300 mb-6">
                Master Java concepts that AI can't replace. Learn to prompt effectively, review AI output, and organize teams with the QUAD Framework.
              </p>

              <div className="grid grid-cols-3 gap-4 mb-8">
                <div className="text-center p-4 bg-slate-800/50 rounded-lg border border-slate-700">
                  <div className="text-2xl font-bold text-blue-400">12</div>
                  <div className="text-sm text-slate-400">Chapters</div>
                </div>
                <div className="text-center p-4 bg-slate-800/50 rounded-lg border border-slate-700">
                  <div className="text-2xl font-bold text-green-400">4+</div>
                  <div className="text-sm text-slate-400">Hours Read</div>
                </div>
                <div className="text-center p-4 bg-slate-800/50 rounded-lg border border-slate-700">
                  <div className="text-2xl font-bold text-purple-400">$0</div>
                  <div className="text-sm text-slate-400">Forever</div>
                </div>
              </div>

              {/* Download Button */}
              {session ? (
                <div className="space-y-3">
                  <button
                    onClick={handleDownload}
                    disabled={downloading}
                    className="w-full px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-bold text-lg transition-all transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
                  >
                    {downloading ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        <span>Preparing Download...</span>
                      </>
                    ) : downloadSuccess ? (
                      <>
                        <span>✓</span>
                        <span>Downloaded! Click to download again</span>
                      </>
                    ) : (
                      <>
                        <span>📥</span>
                        <span>Download Free PDF</span>
                      </>
                    )}
                  </button>
                  <p className="text-sm text-slate-400 text-center">
                    Logged in as {session.user?.email}
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  <Link
                    href="/auth/login?callbackUrl=/book"
                    className="block w-full px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-bold text-lg text-center transition-all transform hover:scale-[1.02]"
                  >
                    Sign In to Download Free →
                  </Link>
                  <p className="text-sm text-slate-400 text-center">
                    No account? <Link href="/auth/signup" className="text-blue-400 hover:text-blue-300">Sign up free</Link>
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* What You'll Learn */}
      <section className="py-16 px-8 bg-slate-800/30">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold mb-8 text-center">What You'll Learn</h2>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                icon: '🎯',
                title: 'Java Deep Dive',
                desc: 'OOP pillars, collections, exceptions - concepts AI gets wrong',
              },
              {
                icon: '🤖',
                title: 'AI Prompting',
                desc: 'Java-specific prompting techniques for better code generation',
              },
              {
                icon: '🔍',
                title: 'Code Review',
                desc: 'Catch AI mistakes - raw types, null checks, wrong patterns',
              },
              {
                icon: '📊',
                title: 'QUAD Framework',
                desc: 'Organize teams around AI with stages, circles, and matrix',
              },
            ].map((item) => (
              <div key={item.title} className="p-6 bg-slate-800/50 rounded-xl border border-slate-700 text-center">
                <div className="text-4xl mb-4">{item.icon}</div>
                <h3 className="font-semibold text-white mb-2">{item.title}</h3>
                <p className="text-sm text-slate-400">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Chapter List */}
      <section className="py-16 px-8">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-2 text-center">12 Chapters</h2>
          <p className="text-slate-400 text-center mb-10">From Java fundamentals to QUAD Framework implementation</p>

          <div className="space-y-4">
            {chapters.map((chapter) => (
              <div
                key={chapter.number}
                className={`bg-slate-800/50 rounded-xl border transition-all ${
                  expandedChapter === chapter.number
                    ? 'border-blue-500/50'
                    : 'border-slate-700 hover:border-slate-600'
                }`}
              >
                <button
                  onClick={() => setExpandedChapter(expandedChapter === chapter.number ? null : chapter.number)}
                  className="w-full p-6 flex items-start gap-4 text-left"
                >
                  {/* Chapter Number */}
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center text-lg font-bold shrink-0 ${
                    chapter.number <= 10
                      ? 'bg-blue-500/20 text-blue-400'
                      : 'bg-green-500/20 text-green-400'
                  }`}>
                    {chapter.number}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-semibold text-white">{chapter.title}</h3>
                      {chapter.badge && (
                        <span className="px-2 py-0.5 bg-green-500/20 text-green-400 rounded text-xs font-medium">
                          {chapter.badge}
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-slate-400">{chapter.description}</p>
                  </div>

                  {/* Read Time & Expand */}
                  <div className="flex items-center gap-3 shrink-0">
                    <span className="text-xs text-slate-500">{chapter.readTime}</span>
                    <span className={`text-slate-400 transition-transform ${
                      expandedChapter === chapter.number ? 'rotate-180' : ''
                    }`}>
                      ▼
                    </span>
                  </div>
                </button>

                {/* Expanded Preview */}
                {expandedChapter === chapter.number && (
                  <div className="px-6 pb-6 pt-0">
                    <div className="pl-16 border-l-2 border-slate-700 ml-6">
                      <p className="text-slate-300 italic">"{chapter.preview}"</p>
                      <p className="text-sm text-slate-500 mt-2">— Chapter {chapter.number} preview</p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Author Section */}
      <section className="py-16 px-8 bg-slate-800/30">
        <div className="max-w-4xl mx-auto">
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="w-32 h-32 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-5xl shrink-0">
              👨‍💻
            </div>
            <div>
              <h3 className="text-2xl font-bold mb-2">About the Author</h3>
              <p className="text-slate-300 mb-4">
                Written by the creator of the QUAD Framework, this book combines 20+ years of Java experience
                with practical insights on AI-assisted development. The goal: help Java developers thrive in
                the AI era by understanding what AI can and cannot do.
              </p>
              <p className="text-slate-400 text-sm">
                The QUAD Framework (Question → Understand → Allocate → Deliver) is now used by teams
                to organize their AI-augmented workflows effectively.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-16 px-8">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Master Java + AI?</h2>
          <p className="text-slate-400 mb-8">
            Download the complete book free. No strings attached. Start learning today.
          </p>

          {session ? (
            <button
              onClick={handleDownload}
              disabled={downloading}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-bold text-lg transition-all transform hover:scale-[1.02] disabled:opacity-50 flex items-center justify-center gap-3 mx-auto"
            >
              {downloading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Preparing...</span>
                </>
              ) : (
                <>
                  <span>📥</span>
                  <span>Download Free PDF</span>
                </>
              )}
            </button>
          ) : (
            <Link
              href="/auth/login?callbackUrl=/book"
              className="inline-block px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-bold text-lg transition-all transform hover:scale-[1.02]"
            >
              Sign In to Download Free →
            </Link>
          )}

          <div className="mt-8 flex items-center justify-center gap-6 text-sm text-slate-500">
            <span>✓ PDF Format</span>
            <span>✓ 12 Chapters</span>
            <span>✓ Free Forever</span>
          </div>
        </div>
      </section>
    </div>
  );
}
