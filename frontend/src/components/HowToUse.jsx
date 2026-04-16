import { Upload, CheckCircle, Settings, Play } from 'lucide-react';

export default function HowToUse() {
    const steps = [
        {
            icon: Upload,
            title: 'Upload Dataset',
            description: 'Upload a CSV file with date and sales columns',
            details: ['Must contain a date column (e.g., Order Date, Date)', 'Must contain numeric values (e.g., Sales, Revenue)', 'Time-based data (daily/weekly/monthly)']
        },
        {
            icon: CheckCircle,
            title: 'Verify Columns',
            description: 'System auto-detects date and target columns',
            details: ['Date column is automatically identified', 'Sales/revenue column is detected', 'Manual selection available if needed']
        },
        {
            icon: Settings,
            title: 'Configure Forecast',
            description: 'Choose model and forecast duration',
            details: ['Select Linear Regression or Random Forest', 'Set forecast horizon (7-90 days)', 'Review detected columns']
        },
        {
            icon: Play,
            title: 'Generate Forecast',
            description: 'Click Run Forecast to see predictions',
            details: ['View forecast chart', 'See performance metrics', 'Get AI-generated insights']
        }
    ];

    return (
        <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-6 border border-indigo-100">
            <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                <span className="text-2xl">📚</span>
                How to Use This Tool
            </h3>

            <div className="space-y-4">
                {steps.map((step, index) => {
                    const Icon = step.icon;
                    return (
                        <div key={index} className="flex gap-4">
                            <div className="flex-shrink-0">
                                <div className="w-10 h-10 rounded-full bg-white shadow-sm flex items-center justify-center">
                                    <Icon className="text-indigo-600" size={20} />
                                </div>
                            </div>
                            <div className="flex-1">
                                <h4 className="font-semibold text-gray-800 mb-1">
                                    {index + 1}. {step.title}
                                </h4>
                                <p className="text-sm text-gray-600 mb-2">{step.description}</p>
                                <ul className="space-y-1">
                                    {step.details.map((detail, idx) => (
                                        <li key={idx} className="text-xs text-gray-500 flex items-start gap-2">
                                            <span className="text-indigo-500 mt-0.5">•</span>
                                            <span>{detail}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    );
                })}
            </div>

            <div className="mt-6 p-4 bg-white rounded-lg border border-indigo-200">
                <p className="text-sm text-gray-700">
                    <span className="font-semibold text-indigo-600">💡 Tip:</span> For best results, ensure your dataset has at least 30 days of historical data.
                </p>
            </div>
        </div>
    );
}
