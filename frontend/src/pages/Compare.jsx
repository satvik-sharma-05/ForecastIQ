import { useState, useEffect } from 'react';
import { GitCompare, Trophy } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import api from '../api/axios';
import EmptyState from '../components/EmptyState';
import { useToast } from '../hooks/useToast';
import Toast from '../components/Toast';

export default function Compare() {
    const [history, setHistory] = useState([]);
    const [selectedIds, setSelectedIds] = useState([]);
    const [comparison, setComparison] = useState(null);
    const [loading, setLoading] = useState(false);
    const { toasts, hideToast, error: showError, warning: showWarning } = useToast();

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const response = await api.get('/forecast/history');
            setHistory(response.data);
        } catch (error) {
            console.error('Failed to fetch history:', error);
        }
    };

    const handleCompare = async () => {
        if (selectedIds.length < 2) {
            showWarning('Please select at least 2 forecasts to compare');
            return;
        }

        setLoading(true);
        try {
            const response = await api.post('/forecast/compare', {
                forecast_ids: selectedIds,
            });
            setComparison(response.data);
        } catch (error) {
            showError('Comparison failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const toggleSelection = (id) => {
        setSelectedIds((prev) =>
            prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
        );
    };

    const chartData = comparison?.forecasts.map((f) => ({
        name: f.model_type.replace('_', ' '),
        MAE: f.metrics.mae,
        RMSE: f.metrics.rmse,
        'R²': f.metrics.r2 * 100,
    }));

    return (
        <div>
            {toasts.map((toast) => (
                <Toast
                    key={toast.id}
                    type={toast.type}
                    message={toast.message}
                    onClose={() => hideToast(toast.id)}
                    duration={toast.duration}
                />
            ))}

            <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-800 mb-2">Compare Forecasts</h1>
                <p className="text-gray-600">Analyze and compare model performance</p>
            </div>

            {history.length === 0 ? (
                <div className="bg-white rounded-xl shadow-lg">
                    <EmptyState
                        type="no-forecast"
                        message="Run at least 2 forecasts to compare their performance"
                    />
                </div>
            ) : (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Selection Panel */}
                    <div className="lg:col-span-1">
                        <div className="bg-white rounded-xl shadow-lg p-6">
                            <h2 className="text-xl font-bold text-gray-800 mb-4">
                                Select Forecasts ({selectedIds.length})
                            </h2>
                            <div className="space-y-2 max-h-96 overflow-y-auto">
                                {history.map((run) => (
                                    <label
                                        key={run.id}
                                        className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-colors ${selectedIds.includes(run.id)
                                            ? 'bg-indigo-50 border-2 border-indigo-500'
                                            : 'bg-gray-50 hover:bg-gray-100'
                                            }`}
                                    >
                                        <input
                                            type="checkbox"
                                            checked={selectedIds.includes(run.id)}
                                            onChange={() => toggleSelection(run.id)}
                                            className="w-4 h-4"
                                        />
                                        <div className="flex-1">
                                            <p className="font-medium text-gray-800 text-sm">{run.dataset_name}</p>
                                            <p className="text-xs text-gray-500 capitalize">
                                                {run.model_type.replace('_', ' ')}
                                            </p>
                                        </div>
                                    </label>
                                ))}
                            </div>
                            <button
                                onClick={handleCompare}
                                disabled={loading || selectedIds.length < 2}
                                className="w-full mt-4 flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50"
                            >
                                <GitCompare size={20} />
                                {loading ? 'Comparing...' : 'Compare'}
                            </button>
                        </div>
                    </div>

                    {/* Results Panel */}
                    <div className="lg:col-span-2">
                        {comparison ? (
                            <div className="space-y-6">
                                {/* Best Model */}
                                <div className="bg-gradient-to-r from-yellow-400 to-orange-500 rounded-xl shadow-lg p-6 text-white">
                                    <div className="flex items-center gap-3 mb-2">
                                        <Trophy size={32} />
                                        <h2 className="text-2xl font-bold">Best Model</h2>
                                    </div>
                                    <p className="text-xl capitalize">{comparison.best_model.model_type.replace('_', ' ')}</p>
                                    <p className="text-sm opacity-90 mt-1">{comparison.best_model.reason}</p>
                                </div>

                                {/* Metrics Chart */}
                                <div className="bg-white rounded-xl shadow-lg p-6">
                                    <h2 className="text-xl font-bold text-gray-800 mb-4">Performance Comparison</h2>
                                    <ResponsiveContainer width="100%" height={300}>
                                        <BarChart data={chartData}>
                                            <CartesianGrid strokeDasharray="3 3" />
                                            <XAxis dataKey="name" />
                                            <YAxis />
                                            <Tooltip />
                                            <Legend />
                                            <Bar dataKey="MAE" fill="#3b82f6" />
                                            <Bar dataKey="RMSE" fill="#8b5cf6" />
                                            <Bar dataKey="R²" fill="#10b981" />
                                        </BarChart>
                                    </ResponsiveContainer>
                                </div>

                                {/* Detailed Metrics */}
                                <div className="bg-white rounded-xl shadow-lg p-6">
                                    <h2 className="text-xl font-bold text-gray-800 mb-4">Detailed Metrics</h2>
                                    <div className="space-y-4">
                                        {comparison.forecasts.map((forecast, idx) => (
                                            <div key={idx} className="p-4 bg-gray-50 rounded-lg">
                                                <h3 className="font-semibold text-gray-800 mb-3 capitalize">
                                                    {forecast.model_type.replace('_', ' ')}
                                                </h3>
                                                <div className="grid grid-cols-3 gap-4">
                                                    <div>
                                                        <p className="text-xs text-gray-500">MAE</p>
                                                        <p className="text-lg font-bold text-blue-600">
                                                            {forecast.metrics.mae.toFixed(2)}
                                                        </p>
                                                    </div>
                                                    <div>
                                                        <p className="text-xs text-gray-500">RMSE</p>
                                                        <p className="text-lg font-bold text-purple-600">
                                                            {forecast.metrics.rmse.toFixed(2)}
                                                        </p>
                                                    </div>
                                                    <div>
                                                        <p className="text-xs text-gray-500">R²</p>
                                                        <p className="text-lg font-bold text-green-600">
                                                            {forecast.metrics.r2.toFixed(3)}
                                                        </p>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="bg-white rounded-xl shadow-lg">
                                <EmptyState
                                    type="no-data"
                                    message="Select at least 2 forecasts from the left panel to compare"
                                />
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
