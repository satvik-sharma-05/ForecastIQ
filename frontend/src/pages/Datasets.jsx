import { useState, useEffect } from 'react';
import { Upload, Trash2, FileText, Calendar } from 'lucide-react';
import api from '../api/axios';
import EmptyState from '../components/EmptyState';
import LoadingSkeleton from '../components/LoadingSkeleton';
import { useToast } from '../hooks/useToast';
import Toast from '../components/Toast';

export default function Datasets() {
    const [datasets, setDatasets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const { toasts, hideToast, error: showError, success: showSuccess } = useToast();

    useEffect(() => {
        fetchDatasets();
    }, []);

    const fetchDatasets = async () => {
        try {
            const response = await api.get('/datasets');
            setDatasets(response.data);
        } catch (error) {
            console.error('Failed to fetch datasets:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        if (!file.name.endsWith('.csv')) {
            showError('Please upload a CSV file');
            return;
        }

        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            await api.post('/datasets/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            showSuccess(`Dataset "${file.name}" uploaded successfully!`);
            fetchDatasets();
        } catch (error) {
            const errorMsg = error.response?.data?.detail || 'Upload failed. Please check your file format.';
            showError(errorMsg);
        } finally {
            setUploading(false);
        }
    };

    const handleDelete = async (id, name) => {
        if (!confirm(`Are you sure you want to delete "${name}"?`)) return;

        try {
            await api.delete(`/datasets/${id}`);
            showSuccess('Dataset deleted successfully');
            fetchDatasets();
        } catch (error) {
            showError('Failed to delete dataset');
        }
    };

    if (loading) {
        return (
            <div>
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-4xl font-bold text-gray-800 mb-2">Datasets</h1>
                        <p className="text-gray-600">Manage your data sources</p>
                    </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[1, 2, 3].map((i) => (
                        <LoadingSkeleton key={i} type="card" />
                    ))}
                </div>
            </div>
        );
    }

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
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-4xl font-bold text-gray-800 mb-2">Datasets</h1>
                    <p className="text-gray-600">Manage your data sources</p>
                </div>
                <label className="cursor-pointer">
                    <input
                        type="file"
                        accept=".csv"
                        onChange={handleUpload}
                        className="hidden"
                        disabled={uploading}
                    />
                    <div className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-lg transition-all">
                        <Upload size={20} />
                        {uploading ? 'Uploading...' : 'Upload CSV'}
                    </div>
                </label>
            </div>

            {datasets.length === 0 ? (
                <div className="bg-white rounded-xl shadow-lg">
                    <EmptyState
                        type="upload"
                        message="Upload your first CSV file with date and sales columns to get started"
                    />
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {datasets.map((dataset) => (
                        <div
                            key={dataset.id}
                            className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
                        >
                            <div className="flex items-start justify-between mb-4">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-indigo-100 rounded-lg">
                                        <FileText className="text-indigo-600" size={24} />
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-gray-800 truncate">{dataset.name}</h3>
                                        <p className="text-sm text-gray-500">{dataset.row_count} rows</p>
                                    </div>
                                </div>
                                <button
                                    onClick={() => handleDelete(dataset.id, dataset.name)}
                                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                >
                                    <Trash2 size={18} />
                                </button>
                            </div>

                            <div className="space-y-2">
                                <div className="flex items-center gap-2 text-sm text-gray-600">
                                    <Calendar size={16} />
                                    {new Date(dataset.uploaded_at).toLocaleDateString()}
                                </div>
                                <div className="flex flex-wrap gap-1">
                                    {dataset.columns.slice(0, 3).map((col, idx) => (
                                        <span
                                            key={idx}
                                            className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                                        >
                                            {col}
                                        </span>
                                    ))}
                                    {dataset.columns.length > 3 && (
                                        <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                                            +{dataset.columns.length - 3} more
                                        </span>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
