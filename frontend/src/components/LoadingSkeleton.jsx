export default function LoadingSkeleton({ type = 'card' }) {
    if (type === 'chart') {
        return (
            <div className="animate-pulse">
                <div className="h-64 bg-gray-200 rounded-lg"></div>
            </div>
        );
    }

    if (type === 'card') {
        return (
            <div className="animate-pulse bg-white rounded-xl shadow-lg p-6">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-2/3"></div>
            </div>
        );
    }

    if (type === 'table') {
        return (
            <div className="animate-pulse space-y-3">
                {[1, 2, 3, 4].map((i) => (
                    <div key={i} className="h-12 bg-gray-200 rounded"></div>
                ))}
            </div>
        );
    }

    return null;
}
