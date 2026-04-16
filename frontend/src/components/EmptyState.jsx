import { FileText, TrendingUp, Upload, AlertCircle } from 'lucide-react';

export default function EmptyState({ type = 'no-data', message, icon: Icon }) {
    const states = {
        'no-data': {
            icon: FileText,
            title: 'No Data Available',
            message: message || 'Upload a dataset to start forecasting',
            color: 'text-gray-400'
        },
        'no-forecast': {
            icon: TrendingUp,
            title: 'No Forecast Generated',
            message: message || 'Run forecast to see predictions and insights',
            color: 'text-indigo-400'
        },
        'upload': {
            icon: Upload,
            title: 'Upload Dataset',
            message: message || 'Upload a CSV file with date and sales columns',
            color: 'text-purple-400'
        },
        'error': {
            icon: AlertCircle,
            title: 'Something Went Wrong',
            message: message || 'Please try again or contact support',
            color: 'text-red-400'
        }
    };

    const state = states[type] || states['no-data'];
    const StateIcon = Icon || state.icon;

    return (
        <div className="flex flex-col items-center justify-center py-16 px-4 animate-fade-in">
            <div className={`p-6 rounded-full bg-gray-50 mb-6 ${state.color}`}>
                <StateIcon size={48} strokeWidth={1.5} />
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">{state.title}</h3>
            <p className="text-gray-600 text-center max-w-md">{state.message}</p>
        </div>
    );
}
