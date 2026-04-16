import { TrendingUp, TrendingDown, AlertCircle, Sparkles, Target } from 'lucide-react';

export default function InsightCard({ insight, index }) {
    const getInsightConfig = (type) => {
        const configs = {
            peak: {
                icon: TrendingUp,
                title: 'Peak Demand Detected',
                gradient: 'from-green-500 to-emerald-600',
                bg: 'bg-green-50',
                iconBg: 'bg-green-100',
                iconColor: 'text-green-600'
            },
            low: {
                icon: TrendingDown,
                title: 'Low Demand Period',
                gradient: 'from-red-500 to-rose-600',
                bg: 'bg-red-50',
                iconBg: 'bg-red-100',
                iconColor: 'text-red-600'
            },
            trend: {
                icon: Sparkles,
                title: 'Trend Detected',
                gradient: 'from-blue-500 to-indigo-600',
                bg: 'bg-blue-50',
                iconBg: 'bg-blue-100',
                iconColor: 'text-blue-600'
            },
            forecast: {
                icon: Target,
                title: 'Forecast Insight',
                gradient: 'from-purple-500 to-pink-600',
                bg: 'bg-purple-50',
                iconBg: 'bg-purple-100',
                iconColor: 'text-purple-600'
            }
        };
        return configs[type] || configs.forecast;
    };

    const config = getInsightConfig(insight.type);
    const Icon = config.icon;

    return (
        <div
            className="group bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 p-6 border border-gray-100 hover:scale-[1.02] animate-fade-in"
            style={{ animationDelay: `${index * 100}ms` }}
        >
            <div className="flex items-start gap-4">
                <div className={`${config.iconBg} p-3 rounded-lg flex-shrink-0 group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className={config.iconColor} size={24} />
                </div>

                <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold text-gray-800">{config.title}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.bg} ${config.iconColor}`}>
                            {insight.type.toUpperCase()}
                        </span>
                    </div>

                    <p className="text-gray-700 leading-relaxed mb-3">
                        {insight.message}
                    </p>

                    {insight.data && (
                        <div className={`${config.bg} rounded-lg p-3 mt-3`}>
                            <div className="grid grid-cols-2 gap-2 text-sm">
                                {Object.entries(insight.data).map(([key, value]) => (
                                    <div key={key}>
                                        <span className="text-gray-600 capitalize">
                                            {key.replace(/_/g, ' ')}:
                                        </span>
                                        <span className={`ml-2 font-semibold ${config.iconColor}`}>
                                            {typeof value === 'number' ? value.toFixed(2) : value}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
