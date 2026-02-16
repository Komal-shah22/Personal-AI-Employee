export function LoadingSkeleton({ type }: { type: 'metrics' | 'grid' | 'feed' | 'actions' | 'charts' | 'approvals' }) {
  switch (type) {
    case 'metrics':
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="metric-card h-[280px]">
              <div className="skeleton h-full" />
            </div>
          ))}
        </div>
      );

    case 'grid':
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="agent-card h-[200px]">
              <div className="skeleton h-full" />
            </div>
          ))}
        </div>
      );

    case 'feed':
      return (
        <div className="card p-6 h-[500px]">
          <div className="skeleton h-full" />
        </div>
      );

    case 'actions':
      return (
        <div className="card p-6">
          <div className="skeleton h-[500px]" />
        </div>
      );

    case 'charts':
      return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="card p-6 h-[400px]">
            <div className="skeleton h-full" />
          </div>
          <div className="card p-6 h-[400px]">
            <div className="skeleton h-full" />
          </div>
        </div>
      );

    case 'approvals':
      return (
        <div className="card p-6">
          <div className="skeleton h-64" />
        </div>
      );

    default:
      return (
        <div className="card p-6">
          <div className="skeleton h-64" />
        </div>
      );
  }
}
