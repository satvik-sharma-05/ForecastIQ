import { useState, useEffect } from 'react';
import { Database, TrendingUp, Lightbulb, Activity } from 'lucide-react';
import api from '../api/axios';
import EmptyState from '../components/EmptyState';
import LoadingSkeleton from '../components/LoadingSkeleton';

export default function Dashboard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const response = await api.get('/dashboard/stats');
            setStats(response.data);
        } catch (error) {
            console.error('Failed to fetch stats:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div>
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-gray-800 mb-2">Dashboard</h1>
                    <p className="text-gray-600">Welcome to your forecasting command center</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    {[1, 2, 3, 4].map((i) => (
                        <LoadingSkeleton key={i} type="card" />
                    ))}
                </div>
            </div>
        );
    }

    const statCards = [
        {
            title: 'Total Datasets',
            value: stats?.total_datasets || 0,
            icon: Database,
            color: 'from-blue-500 to-blue-600',
            bgColor: 'bg-blue-50',
        },
        {
            title: 'Forecasts Run',
            value: stats?.total_forecasts || 0,
            icon: TrendingUp,
            color: 'from-purple-500 to-purple-600',
            bgColor: 'bg-purple-50',
        },
        {
            title: 'Insights Generated',
            value: stats?.total_insights || 0,
            icon: Lightbulb,
            color: 'from-yellow-500 to-yellow-600',
            bgColor: 'bg-yellow-50',
        },
        {
            title: 'Recent Activity',
            value: stats?.recent_activity?.length || 0,
            icon: Activity,
            color: 'from-green-500 to-green-600',
            bgColor: 'bg-green-50',
        },
    ];

    return (
        <div>
            <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-800 mb-2">Dashboard</h1>
                <p className="text-gray-600">Welcome to your forecasting command center</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {statCards.map((stat, index) => {
                    const Icon = stat.icon;
                    return (
                        <div
                            key={index}
                            className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
                        >
                            <div className="flex items-center justify-between mb-4">
                                <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                                    <Icon className={`bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`} size={24} />
                                </div>
                            </div>
                            <h3 className="text-gray-600 text-sm font-medium mb-1">{stat.title}</h3>
                            <p className="text-3xl font-bold text-gray-800">{stat.value}</p>
                        </div>
                    );
                })}
            </div>

            {/* Recent Activity */}
            <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Recent Forecasts</h2>
                {stats?.recent_activity && stats.recent_activity.length > 0 ? (
                    <div className="space-y-3">
                        {stats.recent_activity.map((activity) => (
                            <div
                                key={activity.id}
                                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                            >
                                <div className="flex items-center gap-3">
                                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                                    <div>
                                        <p className="font-medium text-gray-800 capitalize">
                                            {activity.model_type.replace('_', ' ')}
                                        </p>
                                        <p className="text-sm text-gray-500">
                                            {new Date(activity.created_at).toLocaleDateString()}
                                        </p>
                                    </div>
                                </div>
                                <span className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium">
                                    Completed
                                </span>
                            </div>
                        ))}
                    </div>
                ) : (
                    <EmptyState
                        type="no-data"
                        message="No forecasts yet. Start by uploading a dataset!"
                    />
                )}
            </div>
        </div>
    );
}
