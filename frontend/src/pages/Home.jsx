import { Link } from 'react-router-dom';
import { TrendingUp, Database, Brain, Zap, BarChart3, Lightbulb, ArrowRight, CheckCircle } from 'lucide-react';

export default function Home() {
    const features = [
        {
            icon: Database,
            title: 'Dataset Management',
            description: 'Upload CSV files with historical sales data. Auto-detect date and target columns.',
            color: 'from-blue-500 to-cyan-500'
        },
        {
            icon: Brain,
            title: 'ML-Powered Forecasting',
            description: 'Pre-trained Linear Regression and Random Forest models for accurate predictions.',
            color: 'from-purple-500 to-pink-500'
        },
        {
            icon: BarChart3,
            title: 'Model Comparison',
            description: 'Compare multiple forecasts side-by-side to find the best performing model.',
            color: 'from-green-500 to-emerald-500'
        },
        {
            icon: Lightbulb,
            title: 'Smart Insights',
            description: 'AI-generated business insights including peak detection and trend analysis.',
            color: 'from-yellow-500 to-orange-500'
        }
    ];

    const steps = [
        {
            number: '01',
            title: 'Upload Your Dataset',
            description: 'Upload a CSV file containing historical data with date and sales columns',
            details: [
                'Supports various date formats',
                'Auto-detects columns',
                'Handles missing values'
            ]
        },
        {
            number: '02',
            title: 'Configure Forecast',
            description: 'Select date column, target column, model type, and forecast horizon',
            details: [
                'Choose Linear Regression or Random Forest',
                'Set forecast period (7-90 days)',
                'Manual column override available'
            ]
        },
        {
            number: '03',
            title: 'Generate Predictions',
            description: 'Run the forecast and view predictions with performance metrics',
            details: [
                'View MAE, RMSE, and R² scores',
                'Interactive forecast charts',
                'Export predictions'
            ]
        },
        {
            number: '04',
            title: 'Analyze Insights',
            description: 'Get AI-generated insights about trends, peaks, and future demand',
            details: [
                'Peak demand detection',
                'Trend analysis',
                'Actionable recommendations'
            ]
        }
    ];

    const techStack = [
        { name: 'React + Vite', category: 'Frontend' },
        { name: 'Tailwind CSS', category: 'Styling' },
        { name: 'FastAPI', category: 'Backend' },
        { name: 'MongoDB', category: 'Database' },
        { name: 'Scikit-learn', category: 'ML' },
        { name: 'JWT Auth', category: 'Security' }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
            {/* Hero Section */}
            <div className="container mx-auto px-4 py-16">
                <div className="text-center mb-16 animate-fade-in">
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium mb-6">
                        <Zap size={16} />
                        ML-Powered Forecasting Platform
                    </div>
                    <h1 className="text-6xl font-bold text-gray-900 mb-6">
                        Welcome to <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">ForecastIQ</span>
                    </h1>
                    <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
                        Transform your historical data into actionable predictions with our intelligent forecasting platform.
                        Upload datasets, run ML models, and get instant insights.
                    </p>
                    <div className="flex gap-4 justify-center">
                        <Link
                            to="/signup"
                            className="flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-semibold hover:shadow-xl transition-all text-lg"
                        >
                            Get Started
                            <ArrowRight size={20} />
                        </Link>
                        <Link
                            to="/login"
                            className="px-8 py-4 bg-white text-gray-800 rounded-lg font-semibold hover:shadow-lg transition-all border-2 border-gray-200 text-lg"
                        >
                            Sign In
                        </Link>
                    </div>
                </div>

                {/* Features Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-20">
                    {features.map((feature, index) => {
                        const Icon = feature.icon;
                        return (
                            <div
                                key={index}
                                className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-all hover:scale-105 animate-fade-in"
                                style={{ animationDelay: `${index * 100}ms` }}
                            >
                                <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4`}>
                                    <Icon className="text-white" size={24} />
                                </div>
                                <h3 className="text-lg font-bold text-gray-800 mb-2">{feature.title}</h3>
                                <p className="text-gray-600 text-sm">{feature.description}</p>
                            </div>
                        );
                    })}
                </div>

                {/* How It Works */}
                <div className="mb-20">
                    <div className="text-center mb-12">
                        <h2 className="text-4xl font-bold text-gray-900 mb-4">How It Works</h2>
                        <p className="text-gray-600 text-lg">Four simple steps to accurate forecasts</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {steps.map((step, index) => (
                            <div
                                key={index}
                                className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all animate-fade-in"
                                style={{ animationDelay: `${index * 150}ms` }}
                            >
                                <div className="flex items-start gap-6">
                                    <div className="text-6xl font-bold text-indigo-100">
                                        {step.number}
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="text-2xl font-bold text-gray-800 mb-2">{step.title}</h3>
                                        <p className="text-gray-600 mb-4">{step.description}</p>
                                        <ul className="space-y-2">
                                            {step.details.map((detail, idx) => (
                                                <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                                                    <CheckCircle className="text-green-500 flex-shrink-0 mt-0.5" size={16} />
                                                    <span>{detail}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Tech Stack */}
                <div className="bg-white rounded-2xl p-12 shadow-xl mb-20">
                    <div className="text-center mb-8">
                        <h2 className="text-3xl font-bold text-gray-900 mb-4">Built With Modern Tech</h2>
                        <p className="text-gray-600">Production-ready stack for scalability and performance</p>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
                        {techStack.map((tech, index) => (
                            <div
                                key={index}
                                className="text-center p-4 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg hover:shadow-md transition-all"
                            >
                                <p className="font-semibold text-gray-800 mb-1">{tech.name}</p>
                                <p className="text-xs text-gray-500">{tech.category}</p>
                            </div>
                        ))}
                    </div>
                </div>

                {/* CTA Section */}
                <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-12 text-center text-white shadow-2xl">
                    <TrendingUp className="mx-auto mb-6" size={64} />
                    <h2 className="text-4xl font-bold mb-4">Ready to Start Forecasting?</h2>
                    <p className="text-xl mb-8 opacity-90">
                        Join ForecastIQ today and transform your data into actionable predictions
                    </p>
                    <Link
                        to="/signup"
                        className="inline-flex items-center gap-2 px-8 py-4 bg-white text-indigo-600 rounded-lg font-semibold hover:shadow-xl transition-all text-lg"
                    >
                        Create Free Account
                        <ArrowRight size={20} />
                    </Link>
                </div>
            </div>

            {/* Footer */}
            <footer className="border-t border-gray-200 py-8">
                <div className="container mx-auto px-4 text-center text-gray-600">
                    <p className="mb-2">© 2026 ForecastIQ. Built with ❤️ for data-driven decisions.</p>
                    <p className="text-sm">Full-stack ML forecasting platform with React, FastAPI, MongoDB & Scikit-learn</p>
                </div>
            </footer>
        </div>
    );
}
