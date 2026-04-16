import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { LayoutDashboard, Database, TrendingUp, History, Lightbulb, GitCompare, LogOut } from 'lucide-react';

export default function Layout({ setToken }) {
    const location = useLocation();
    const navigate = useNavigate();

    const handleLogout = () => {
        setToken(null);
        localStorage.removeItem('token');
        navigate('/login');
    };

    const navItems = [
        { path: '/app', icon: LayoutDashboard, label: 'Dashboard' },
        { path: '/app/datasets', icon: Database, label: 'Datasets' },
        { path: '/app/forecast', icon: TrendingUp, label: 'Forecast' },
        { path: '/app/history', icon: History, label: 'History' },
        { path: '/app/insights', icon: Lightbulb, label: 'Insights' },
        { path: '/app/compare', icon: GitCompare, label: 'Compare' },
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
            {/* Sidebar */}
            <aside className="fixed left-0 top-0 h-full w-64 bg-white shadow-xl border-r border-gray-200 z-10">
                <div className="p-6">
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                        ForecastIQ
                    </h1>
                    <p className="text-sm text-gray-500 mt-1">ML-Powered Forecasting</p>
                </div>

                <nav className="px-3 space-y-1">
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        const isActive = location.pathname === item.path;
                        return (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${isActive
                                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg'
                                    : 'text-gray-700 hover:bg-gray-100'
                                    }`}
                            >
                                <Icon size={20} />
                                <span className="font-medium">{item.label}</span>
                            </Link>
                        );
                    })}
                </nav>

                <div className="absolute bottom-6 left-3 right-3">
                    <button
                        onClick={handleLogout}
                        className="flex items-center gap-3 px-4 py-3 w-full rounded-lg text-red-600 hover:bg-red-50 transition-all"
                    >
                        <LogOut size={20} />
                        <span className="font-medium">Logout</span>
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="ml-64 p-8">
                <Outlet />
            </main>
        </div>
    );
}
