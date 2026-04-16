import { useEffect } from 'react';
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react';

export default function Toast({ type = 'info', message, onClose, duration = 5000 }) {
    useEffect(() => {
        if (duration > 0) {
            const timer = setTimeout(onClose, duration);
            return () => clearTimeout(timer);
        }
    }, [duration, onClose]);

    const types = {
        success: {
            icon: CheckCircle,
            bg: 'bg-green-50',
            border: 'border-green-200',
            text: 'text-green-800',
            iconColor: 'text-green-500'
        },
        error: {
            icon: XCircle,
            bg: 'bg-red-50',
            border: 'border-red-200',
            text: 'text-red-800',
            iconColor: 'text-red-500'
        },
        warning: {
            icon: AlertCircle,
            bg: 'bg-yellow-50',
            border: 'border-yellow-200',
            text: 'text-yellow-800',
            iconColor: 'text-yellow-500'
        },
        info: {
            icon: Info,
            bg: 'bg-blue-50',
            border: 'border-blue-200',
            text: 'text-blue-800',
            iconColor: 'text-blue-500'
        }
    };

    const config = types[type] || types.info;
    const Icon = config.icon;

    return (
        <div className={`fixed top-4 right-4 z-50 animate-slide-in-right max-w-md`}>
            <div className={`${config.bg} ${config.border} border rounded-lg shadow-lg p-4 flex items-start gap-3`}>
                <Icon className={config.iconColor} size={20} />
                <p className={`${config.text} flex-1 text-sm`}>{message}</p>
                <button
                    onClick={onClose}
                    className={`${config.text} hover:opacity-70 transition-opacity`}
                >
                    <X size={18} />
                </button>
            </div>
        </div>
    );
}
