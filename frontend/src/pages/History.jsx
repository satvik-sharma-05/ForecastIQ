import { useState, useEffect } from 'react';
import { TrendingUp } from 'lucide-react';
import api from '../api/axios';
import EmptyState from '../components/EmptyState';
import LoadingSkeleton from '../components/LoadingSkeleton';

export default function History() {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const response = await api.get('/forecast/history');
            setHistory(response.data);
        } catch (error) {
            console.error('Failed to fetch history:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div>
                <div className="mb-8">
                    <h1 className="text-4xl font-bold text-gray-800 mb-2">Forecast History</h1>
                    <p className="text-gray-600">View all your past forecast runs</p>
                </div>
                <div className="space-y-4">
                    {[1, 2, 3].map((i) => (
                        <LoadingSkeleton key={i} type="card" />
                    ))}
                </div>
            </div>
        );
    }

    return (
        <div>
            <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-800 mb-2">Forecast History</h1>
                <p className="text-gray-600">View all your past forecast runs</p>
            </div>

            {history.length === 0 ? (
                <div className="bg-white rounded-xl shadow-lg">
                    <EmptyState
                        type="no-forecast"
                        message="Run your first forecast to see it here"
                    />
                </div>
            ) : (
                <div className="space-y-4">
                    {history.map((run) => (
                        <div
                            key={run.id}
                            className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
                        >
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="p-3 bg-indigo-100 rounded-lg">
                                        <TrendingUp className="text-indigo-600" size={24} />
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-gray-800 text-lg">
                                            {run.dataset_name}
                                        </h3>
                                        <p className="text-sm text-gray-500 capitalize">
                                            {run.model_type.replace('_', ' ')} • {run.forecast_days} days
                                        </p>
                                        <p className="text-xs text-gray-400 mt-1">
                                            {new Date(run.created_at).toLocaleString()}
                                        </p>
                                    </div>
                                </div>

                                <div className="flex gap-6">
                                    <div className="text-center">
                                        <p className="text-xs text-gray-500 mb-1">MAE</p>
                                        <p className="text-lg font-bold text-blue-600">
                                            {run.metrics.mae.toFixed(2)}
                                        </p>
                                    </div>
                                    <div className="text-center">
                                        <p className="text-xs text-gray-500 mb-1">RMSE</p>
                                        <p className="text-lg font-bold text-purple-600">
                                            {run.metrics.rmse.toFixed(2)}
                                        </p>
                                    </div>
                                    <div className="text-center">
                                        <p className="text-xs text-gray-500 mb-1">R²</p>
                                        <p className="text-lg font-bold text-green-600">
                                            {run.metrics.r2.toFixed(3)}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
