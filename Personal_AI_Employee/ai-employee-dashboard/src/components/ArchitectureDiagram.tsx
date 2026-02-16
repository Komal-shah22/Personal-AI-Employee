'use client';

import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';

const Row1 = [
  { icon: '👁️', name: 'Watcher Agents', role: 'Monitor inputs' },
  { icon: '📝', name: 'Obsidian Vault', role: 'Central storage' },
  { icon: '🤖', name: 'Claude Code', role: 'AI processing' },
];

const Row2 = [
  { icon: '⚡', name: 'Skill Agents', role: 'Execute tasks' },
  { icon: '✋', name: 'HITL Approval', role: 'Human review' },
  { icon: '🔌', name: 'MCP Agents', role: 'External APIs' },
];

function FlowNode({ icon, name, role }: { icon: string; name: string; role: string }) {
  return (
    <motion.div
      whileHover={{ scale: 1.05, y: -2 }}
      className="bg-surface2 border border-border rounded-lg p-4 text-center min-w-[140px] transition-all duration-200"
    >
      <div className="text-2xl mb-2">{icon}</div>
      <div className="font-semibold text-sm mb-1">{name}</div>
      <div className="text-[10px] text-muted">{role}</div>
    </motion.div>
  );
}

export default function ArchitectureDiagram() {
  return (
    <div className="card p-8">
      <h2 className="font-syne font-bold text-xl text-accent mb-6 flex items-center gap-2">
        <span>⚙️</span>
        System Architecture — Sabhi Agents Ka Flow
      </h2>

      <div className="space-y-6">
        {/* Row 1 */}
        <div className="flex items-center justify-center gap-4 flex-wrap">
          {Row1.map((node, index) => (
            <div key={node.name} className="flex items-center gap-4">
              <FlowNode {...node} />
              {index < Row1.length - 1 && (
                <ArrowRight className="text-muted w-5 h-5 hidden md:block" />
              )}
            </div>
          ))}
        </div>

        {/* Row 2 */}
        <div className="flex items-center justify-center gap-4 flex-wrap">
          {Row2.map((node, index) => (
            <div key={node.name} className="flex items-center gap-4">
              <FlowNode {...node} />
              {index < Row2.length - 1 && (
                <ArrowRight className="text-muted w-5 h-5 hidden md:block" />
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
