import { useState, useEffect } from 'react';
import { Play } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import api from '../api/axios';
import HowToUse from '../components/HowToUse';
import EmptyState from '../components/EmptyState';
import LoadingSkeleton from '../components/LoadingSkeleton';
import { useToast } from '../hooks/useToast';
import Toast from '../components/Toast';

export default function Forecast() {
    const [datasets, setDatasets] = useState([]);
    const [selectedDataset, setSelectedDataset] = useState('');
    const [dateColumn, setDateColumn] = useState('');
    const [targetColumn, setTargetColumn] = useState('');
    const [modelType, setModelType] = useState('random_forest');
    const [forecastDays, setForecastDays] = useState(30);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [columns, setColumns] = useState([]);
    const { toasts, hideToast, error: showError, success: showSuccess } = useToast();

    useEffect(() => {
        fetchDatasets();
    }, []);

    useEffect(() => {
        if (selectedDataset) {
            const dataset = datasets.find(d => d.id === selectedDataset);
            if (dataset) {
                setColumns(dataset.columns);
            }
        }
    }, [selectedDataset, datasets]);

    const fetchDatasets = async () => {
        try {
            const response = await api.get('/datasets');
            setDatasets(response.data);
        } catch (error) {
            console.error('Failed to fetch datasets:', error);
        }
    };

    const handleRunForecast = async () => {
        if (!selectedDataset || !dateColumn || !targetColumn) {
            showError('Please select dataset, date column, and target column');
            return;
        }

        setLoading(true);
        try {
            const response = await api.post('/forecast/run', {
                dataset_id: selectedDataset,
                date_column: dateColumn,
                target_column: targetColumn,
                model_type: modelType,
                forecast_days: forecastDays,
            });
            setResult(response.data);
            showSuccess('Forecast generated successfully!');
        } catch (error) {
            const errorMsg = error.response?.data?.detail || 'Failed to generate forecast. Please check your dataset format.';
            showError(errorMsg);
        } finally {
            setLoading(false);
        }
    };

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
                <h1 className="text-4xl font-bold text-gray-800 mb-2">Run Forecast</h1>
                <p className="text-gray-600">Configure and execute ML predictions</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Configuration Panel */}
                <div className="lg:col-span-1 space-y-6">
                    <HowToUse />

                    <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
                        <h2 className="text-xl font-bold text-gray-800 mb-4">Configuration</h2>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Dataset</label>
                            <select
                                value={selectedDataset}
                                onChange={(e) => setSelectedDataset(e.target.value)}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                            >
                                <option value="">Select dataset</option>
                                {datasets.map((d) => (
                                    <option key={d.id} value={d.id}>{d.name}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Date Column</label>
                            <select
                                value={dateColumn}
                                onChange={(e) => setDateColumn(e.target.value)}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                disabled={!selectedDataset}
                            >
                                <option value="">Select column</option>
                                {columns.map((col) => (
                                    <option key={col} value={col}>{col}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Target Column</label>
                            <select
                                value={targetColumn}
                                onChange={(e) => setTargetColumn(e.target.value)}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                disabled={!selectedDataset}
                            >
                                <option value="">Select column</option>
                                {columns.map((col) => (
                                    <option key={col} value={col}>{col}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Model Type</label>
                            <select
                                value={modelType}
                                onChange={(e) => setModelType(e.target.value)}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                            >
                                <option value="linear_regression">Linear Regression</option>
                                <option value="random_forest">Random Forest</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Forecast Days: {forecastDays}
                            </label>
                            <input
                                type="range"
                                min="7"
                                max="90"
                                value={forecastDays}
                                onChange={(e) => setForecastDays(Number(e.target.value))}
                                className="w-full"
                            />
                        </div>

                        <button
                            onClick={handleRunForecast}
                            disabled={loading}
                            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all disabled:opacity-50"
                        >
                            <Play size={20} />
                            {loading ? 'Running...' : 'Run Forecast'}
                        </button>
                    </div>
                </div>

                {/* Results Panel */}
                <div className="lg:col-span-2">
                    {loading ? (
                        <div className="space-y-6">
                            <LoadingSkeleton type="card" />
                            <LoadingSkeleton type="chart" />
                        </div>
                    ) : result ? (
                        <div className="space-y-6">
                            {/* Metrics */}
                            <div className="bg-white rounded-xl shadow-lg p-6">
                                <h2 className="text-xl font-bold text-gray-800 mb-4">Model Performance</h2>
                                <div className="grid grid-cols-3 gap-4">
                                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                                        <p className="text-sm text-gray-600 mb-1">MAE</p>
                                        <p className="text-2xl font-bold text-blue-600">
                                            {result.metrics.mae.toFixed(2)}
                                        </p>
                                    </div>
                                    <div className="text-center p-4 bg-purple-50 rounded-lg">
                                        <p className="text-sm text-gray-600 mb-1">RMSE</p>
                                        <p className="text-2xl font-bold text-purple-600">
                                            {result.metrics.rmse.toFixed(2)}
                                        </p>
                                    </div>
                                    <div className="text-center p-4 bg-green-50 rounded-lg">
                                        <p className="text-sm text-gray-600 mb-1">R²</p>
                                        <p className="text-2xl font-bold text-green-600">
                                            {result.metrics.r2.toFixed(3)}
                                        </p>
                                    </div>
                                </div>
                            </div>

                            {/* Chart */}
                            <div className="bg-white rounded-xl shadow-lg p-6">
                                <h2 className="text-xl font-bold text-gray-800 mb-4">Forecast Visualization</h2>
                                <ResponsiveContainer width="100%" height={300}>
                                    <LineChart data={result.predictions}>
                                        <CartesianGrid strokeDasharray="3 3" />
                                        <XAxis dataKey="date" />
                                        <YAxis />
                                        <Tooltip />
                                        <Legend />
                                        <Line type="monotone" dataKey="predicted_value" stroke="#8b5cf6" strokeWidth={2} />
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>

                            {/* Insights */}
                            {result.insights && result.insights.length > 0 && (
                                <div className="bg-white rounded-xl shadow-lg p-6">
                                    <h2 className="text-xl font-bold text-gray-800 mb-4">Insights</h2>
                                    <div className="space-y-3">
                                        {result.insights.map((insight, idx) => (
                                            <div key={idx} className="p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                                                <p className="text-gray-800">{insight.message}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="bg-white rounded-xl shadow-lg">
                            <EmptyState
                                type="no-forecast"
                                message="Configure settings on the left and click Run Forecast to see predictions"
                            />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
