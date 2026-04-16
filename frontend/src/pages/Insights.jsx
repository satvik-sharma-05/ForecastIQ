import { useState, useEffect } from 'react';
import api from '../api/axios';
import InsightCard from '../components/InsightCard';
import EmptyState from '../components/EmptyState';
import LoadingSkeleton from '../components/LoadingSkeleton';

export default function Insights() {
    const [insights, setInsights] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchInsights();
    }, []);

    const fetchInsights = async () => {
        try {
            const response = await api.get('/insights');
            setInsights(response.data);
        } catch (error) {
            console.error('Failed to fetch insights:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div>
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-gray-800 mb-2">Smart Insights</h1>
                    <p className="text-gray-600">AI-generated business intelligence from your forecasts</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {[1, 2, 3, 4].map((i) => (
                        <LoadingSkeleton key={i} type="card" />
                    ))}
                </div>
            </div>
        );
    }

    return (
        <div>
            <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-800 mb-2">Smart Insights</h1>
                <p className="text-gray-600">AI-generated business intelligence from your forecasts</p>
            </div>

            {insights.length === 0 ? (
                <div className="bg-white rounded-xl shadow-lg">
                    <EmptyState
                        type="no-forecast"
                        message="Run forecasts to generate intelligent insights about your data"
                    />
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {insights.map((insight, index) => (
                        <InsightCard key={insight.id} insight={insight} index={index} />
                    ))}
                </div>
            )}
        </div>
    );
}
