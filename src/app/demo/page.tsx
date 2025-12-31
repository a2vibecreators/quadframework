export default function QUADDemo() {
  return (
    <div className="min-h-screen text-white p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12 text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <span className="text-3xl">🌐</span>
            <h1 className="text-4xl font-bold">QUAD Dashboard Demo</h1>
          </div>
          <p className="text-slate-400">
            See how a QUAD implementation dashboard might look
          </p>
        </div>

        {/* Dashboard Header */}
        <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-white">Project: NutriNine Mobile App</h2>
              <p className="text-sm text-slate-400">Cycle 3 | Week 2 of 4 | Flow Rate: 8.5 pts/day</p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-400">92%</div>
                <div className="text-xs text-slate-500">On Track</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-400">14</div>
                <div className="text-xs text-slate-500">Days Left</div>
              </div>
            </div>
          </div>
        </div>

        {/* Circle Status */}
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          {[
            {
              name: "Management",
              status: "Active",
              agents: { active: 3, total: 4 },
              tasks: { done: 12, total: 15 },
              color: "blue"
            },
            {
              name: "Development",
              status: "Active",
              agents: { active: 4, total: 4 },
              tasks: { done: 28, total: 35 },
              color: "green"
            },
            {
              name: "QA",
              status: "Active",
              agents: { active: 3, total: 4 },
              tasks: { done: 45, total: 52 },
              color: "yellow"
            },
            {
              name: "Infrastructure",
              status: "Idle",
              agents: { active: 2, total: 4 },
              tasks: { done: 8, total: 8 },
              color: "purple"
            },
          ].map((circle) => (
            <div key={circle.name} className={`bg-${circle.color}-500/10 rounded-xl p-4 border border-${circle.color}-500/20`}>
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-bold text-white">{circle.name}</h3>
                <span className={`px-2 py-0.5 rounded-full text-xs ${
                  circle.status === "Active" ? "bg-green-500/20 text-green-300" : "bg-slate-500/20 text-slate-400"
                }`}>
                  {circle.status}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Agents</span>
                  <span className="text-white">{circle.agents.active}/{circle.agents.total}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Tasks</span>
                  <span className="text-white">{circle.tasks.done}/{circle.tasks.total}</span>
                </div>
                <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                  <div
                    className={`h-full bg-${circle.color}-500`}
                    style={{ width: `${(circle.tasks.done / circle.tasks.total) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Agent Activity */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Recent Agent Actions */}
          <div className="bg-slate-800/30 rounded-xl p-6 border border-slate-700">
            <h3 className="font-bold text-white mb-4">Recent Agent Activity</h3>
            <div className="space-y-3">
              {[
                { agent: "Story Agent", action: "Expanded user story US-142", time: "2 min ago", status: "success" },
                { agent: "Dev Agent (API)", action: "Scaffolded AuthController", time: "5 min ago", status: "success" },
                { agent: "UI Test Agent", action: "Running login flow tests...", time: "Now", status: "running" },
                { agent: "Code Review Agent", action: "Reviewed PR #89", time: "12 min ago", status: "success" },
                { agent: "Deploy Agent", action: "Deployed to DEV", time: "15 min ago", status: "success" },
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-3 bg-slate-900/30 rounded-lg p-3">
                  <div className={`w-2 h-2 rounded-full ${
                    item.status === "success" ? "bg-green-400" :
                    item.status === "running" ? "bg-blue-400 animate-pulse" : "bg-slate-400"
                  }`}></div>
                  <div className="flex-1">
                    <div className="flex justify-between">
                      <span className="font-medium text-white text-sm">{item.agent}</span>
                      <span className="text-xs text-slate-500">{item.time}</span>
                    </div>
                    <p className="text-xs text-slate-400">{item.action}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Pending Human Gates */}
          <div className="bg-slate-800/30 rounded-xl p-6 border border-slate-700">
            <h3 className="font-bold text-white mb-4">Pending Human Gates</h3>
            <div className="space-y-3">
              {[
                { gate: "Code Review", item: "PR #91 - Add medication reminder", by: "Tech Lead", urgent: true },
                { gate: "Story Approval", item: "US-145 - Push notifications", by: "BA", urgent: false },
                { gate: "QA Sign-off", item: "Sprint 3 - Health dashboard", by: "QA Lead", urgent: false },
              ].map((item, i) => (
                <div key={i} className={`rounded-lg p-3 border ${
                  item.urgent ? "bg-orange-500/10 border-orange-500/20" : "bg-blue-500/10 border-blue-500/20"
                }`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className={`text-sm font-medium ${item.urgent ? "text-orange-300" : "text-blue-300"}`}>
                      {item.gate}
                    </span>
                    {item.urgent && (
                      <span className="px-2 py-0.5 bg-orange-500/20 text-orange-300 rounded text-xs">Urgent</span>
                    )}
                  </div>
                  <p className="text-sm text-white">{item.item}</p>
                  <p className="text-xs text-slate-500">Waiting for: {item.by}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Cycle Queue */}
        <div className="bg-slate-800/30 rounded-xl p-6 border border-slate-700 mb-8">
          <h3 className="font-bold text-white mb-4">Cycle Queue (Current Cycle)</h3>
          <div className="grid grid-cols-5 gap-4">
            {[
              { status: "Done", count: 18, color: "green" },
              { status: "In Progress", count: 7, color: "blue" },
              { status: "In Review", count: 4, color: "purple" },
              { status: "Ready", count: 8, color: "yellow" },
              { status: "Blocked", count: 2, color: "red" },
            ].map((col) => (
              <div key={col.status} className="text-center">
                <div className={`text-3xl font-bold text-${col.color}-400 mb-1`}>{col.count}</div>
                <div className="text-sm text-slate-400">{col.status}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Flow Documents */}
        <div className="bg-slate-800/30 rounded-xl p-6 border border-slate-700 mb-8">
          <h3 className="font-bold text-white mb-4">Recent Flow Documents</h3>
          <div className="space-y-2">
            {[
              { id: "FLOW_AUTH_001", name: "User Authentication Flow", status: "Active", tests: 24, coverage: 100 },
              { id: "FLOW_HEALTH_002", name: "Health Report Upload", status: "Active", tests: 18, coverage: 94 },
              { id: "FLOW_MEAL_003", name: "Meal Planning", status: "Draft", tests: 0, coverage: 0 },
              { id: "FLOW_NOTIF_004", name: "Push Notifications", status: "In Review", tests: 12, coverage: 75 },
            ].map((flow) => (
              <div key={flow.id} className="flex items-center justify-between bg-slate-900/30 rounded-lg p-3">
                <div>
                  <div className="flex items-center gap-2">
                    <code className="text-xs text-blue-300">{flow.id}</code>
                    <span className={`px-2 py-0.5 rounded text-xs ${
                      flow.status === "Active" ? "bg-green-500/20 text-green-300" :
                      flow.status === "Draft" ? "bg-slate-500/20 text-slate-400" :
                      "bg-yellow-500/20 text-yellow-300"
                    }`}>
                      {flow.status}
                    </span>
                  </div>
                  <p className="text-sm text-white mt-1">{flow.name}</p>
                </div>
                <div className="text-right">
                  <div className="text-sm text-white">{flow.tests} tests</div>
                  <div className={`text-xs ${flow.coverage >= 90 ? "text-green-400" : flow.coverage > 0 ? "text-yellow-400" : "text-slate-500"}`}>
                    {flow.coverage}% coverage
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Info Box */}
        <div className="bg-blue-500/10 rounded-xl p-6 border border-blue-500/20 text-center">
          <h3 className="font-bold text-white mb-2">This is a Demo</h3>
          <p className="text-slate-400 text-sm">
            This dashboard shows what a real QUAD implementation might look like.
            All data is simulated for demonstration purposes.
          </p>
        </div>
      </div>
    </div>
  );
}
