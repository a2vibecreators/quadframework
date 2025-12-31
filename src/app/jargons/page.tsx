export default function QUADJargons() {
  const glossary = [
    { old: "Sprint", quad: "Cycle", meaning: "4-week period of continuous work" },
    { old: "Daily Standup", quad: "Pulse", meaning: "Optional weekly sync (5-15 min)" },
    { old: "Sprint Planning", quad: "Trajectory", meaning: "Setting priorities for the cycle" },
    { old: "Sprint Review", quad: "Checkpoint", meaning: "Monthly demo + release decision" },
    { old: "Retrospective", quad: "Calibration", meaning: "Monthly reflection + improvement" },
    { old: "Backlog", quad: "Horizon", meaning: "Work ahead, prioritized queue" },
    { old: "Backlog Grooming", quad: "Refinement", meaning: "Breaking down and clarifying work" },
    { old: "Sprint Backlog", quad: "Cycle Queue", meaning: "Work selected for current cycle" },
    { old: "Story Points", quad: "Complexity", meaning: "Estimation using chosen method" },
    { old: "Velocity", quad: "Flow Rate", meaning: "Speed of work through pipeline" },
    { old: "Burndown", quad: "Progression", meaning: "Visual of work remaining" },
    { old: "Definition of Done", quad: "Completion Criteria", meaning: "When work is truly done" },
    { old: "Scrum Master", quad: "Scheduling Agent", meaning: "AI handles coordination" },
    { old: "Product Owner", quad: "Circle Lead", meaning: "BA/PM/TL in Management Circle" },
  ];

  const events = [
    { name: "Pulse", freq: "Weekly (optional)", duration: "5-15 min", purpose: "Quick sync, blockers, AI dashboard review" },
    { name: "Checkpoint", freq: "Monthly", duration: "1 hour", purpose: "Demo to stakeholders, release decision" },
    { name: "Calibration", freq: "Monthly", duration: "30-60 min", purpose: "Retrospective, agent learning review" },
    { name: "Trajectory", freq: "Monthly", duration: "1-2 hours", purpose: "Planning priorities for next cycle" },
  ];

  return (
    <div className="min-h-screen text-white p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-3xl">📖</span>
            <h1 className="text-4xl font-bold">QUAD Terminology</h1>
          </div>
          <p className="text-slate-400">
            QUAD uses new terms instead of Scrum jargon - cleaner, clearer, AI-native
          </p>
        </div>

        {/* Quick Reference Card */}
        <section className="mb-12">
          <div className="bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-xl p-6 border border-blue-500/20">
            <h2 className="text-xl font-bold mb-4 text-center">Quick Reference Card</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
              {[
                { term: "CYCLE", def: "4-week period of continuous work" },
                { term: "PULSE", def: "Optional weekly sync (5-15 min)" },
                { term: "TRAJECTORY", def: "Setting priorities for the cycle" },
                { term: "CHECKPOINT", def: "Monthly demo + release decision" },
                { term: "CALIBRATION", def: "Monthly reflection + improvement" },
                { term: "HORIZON", def: "Work backlog (what's ahead)" },
                { term: "REFINEMENT", def: "Breaking down and clarifying work" },
                { term: "CYCLE QUEUE", def: "Work selected for current cycle" },
                { term: "FLOW RATE", def: "Speed of work through pipeline" },
                { term: "PROGRESSION", def: "Visual of work remaining" },
                { term: "OPERATORS", def: "Human specialists who execute circle functions" },
                { term: "CIRCLES", def: "4 functional teams (Mgmt, Dev, QA, Infra)" },
                { term: "AGENTS", def: "AI helpers assigned to each circle" },
                { term: "ENABLING TEAMS", def: "Optional support groups (Arch, Security, etc.)" },
              ].map((item) => (
                <div key={item.term} className="bg-slate-800/50 rounded-lg p-3">
                  <div className="font-bold text-blue-300">{item.term}</div>
                  <div className="text-xs text-slate-400">{item.def}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Full Glossary Table */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-6 text-blue-300">Terminology Mapping</h2>
          <div className="bg-slate-800/30 rounded-xl border border-slate-700 overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-slate-800/50">
                <tr>
                  <th className="px-4 py-3 text-left text-slate-400">Old Term (Scrum)</th>
                  <th className="px-4 py-3 text-left text-blue-300">QUAD Term</th>
                  <th className="px-4 py-3 text-left text-slate-400">Meaning</th>
                </tr>
              </thead>
              <tbody>
                {glossary.map((item, i) => (
                  <tr key={item.quad} className={i % 2 === 0 ? "bg-slate-800/20" : ""}>
                    <td className="px-4 py-3 text-slate-500 line-through">{item.old}</td>
                    <td className="px-4 py-3 font-semibold text-white">{item.quad}</td>
                    <td className="px-4 py-3 text-slate-400">{item.meaning}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* The 4 Circles */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-6 text-blue-300">The 4 Circles</h2>
          <div className="grid grid-cols-2 gap-4">
            {[
              { num: 1, name: "MANAGEMENT", ratio: "B80% / T20%", mode: "Dedicated", desc: "BA, PM, Tech Lead", color: "blue" },
              { num: 2, name: "DEVELOPMENT", ratio: "B30% / T70%", mode: "Mostly Dedicated", desc: "Full Stack, Backend, UI, Mobile", color: "green" },
              { num: 3, name: "QA", ratio: "B30% / T70%", mode: "Mostly Shared", desc: "QA Engineer, Automation, Perf, Security", color: "yellow" },
              { num: 4, name: "INFRASTRUCTURE", ratio: "B20% / T80%", mode: "Always Shared", desc: "DevOps, SRE, Cloud, DBA", color: "purple" },
            ].map((c) => (
              <div key={c.num} className={`bg-${c.color}-500/10 rounded-xl p-4 border border-${c.color}-500/20`}>
                <div className="flex items-center gap-3 mb-2">
                  <div className={`w-8 h-8 rounded-full bg-${c.color}-500/20 flex items-center justify-center text-${c.color}-300 font-bold text-sm`}>
                    {c.num}
                  </div>
                  <div className="font-bold text-white">{c.name} Circle</div>
                </div>
                <div className="text-xs text-slate-500">{c.ratio}</div>
                <div className={`text-xs text-${c.color}-300 font-medium`}>{c.mode}</div>
                <div className="text-xs text-slate-400 mt-1">{c.desc}</div>
              </div>
            ))}
          </div>
          <p className="text-xs text-slate-500 mt-4 text-center">
            B = Business Focus | T = Technical Focus
          </p>
        </section>

        {/* Cycle Events */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-6 text-blue-300">Cycle Events</h2>
          <div className="space-y-4">
            {events.map((event) => (
              <div key={event.name} className="bg-slate-700/30 rounded-xl p-4 border border-slate-600/50 flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-white">{event.name}</h3>
                  <p className="text-sm text-slate-400">{event.purpose}</p>
                </div>
                <div className="text-right">
                  <div className="text-sm text-blue-300">{event.freq}</div>
                  <div className="text-xs text-slate-500">{event.duration}</div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Estimation Methods */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-6 text-blue-300">Estimation Methods</h2>
          <p className="text-slate-400 mb-4">QUAD offers multiple estimation methods. Teams choose in settings:</p>
          <div className="grid md:grid-cols-2 gap-4">
            {[
              {
                name: "Platonic Solids (Default)",
                items: ["Tetrahedron (4) = Trivial", "Cube (6) = Moderate", "Octahedron (8) = Medium", "Dodecahedron (12) = Complex", "Icosahedron (20) = Very Complex"],
              },
              {
                name: "Dimensions",
                items: ["Point (0D) = Trivial", "Line (1D) = Simple", "Triangle (2D) = Moderate", "Cube (3D) = Complex", "Tesseract (4D) = Very Complex"],
              },
              {
                name: "Powers",
                items: ["2^0 = 1 (Trivial)", "2^1 = 2 (Simple)", "2^2 = 4 (Moderate)", "2^3 = 8 (Complex)", "2^4 = 16 (Very Complex)"],
              },
              {
                name: "Classic Fibonacci",
                items: ["1 = Trivial", "2 = Simple", "3 = Moderate", "5 = Medium", "8 = Complex", "13 = Very Complex"],
              },
            ].map((method) => (
              <div key={method.name} className="bg-slate-800/30 rounded-xl p-4 border border-slate-700">
                <h3 className="font-bold text-white mb-3">{method.name}</h3>
                <ul className="space-y-1 text-sm text-slate-400">
                  {method.items.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
