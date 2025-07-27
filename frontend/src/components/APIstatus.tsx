import React, { useState, useEffect } from 'react';
import { Wifi, WifiOff, AlertCircle } from 'lucide-react';
import { apiService } from '../services/api';

const APIStatus: React.FC = () => {
  const [status, setStatus] = useState<'connected' | 'disconnected' | 'checking'>('checking');
  const [apiInfo, setApiInfo] = useState<{
    message: string;
    version: string;
    author: string;
  } | null>(null);

  const checkAPIStatus = async () => {
    try {
      setStatus('checking');
      const [healthResponse, infoResponse] = await Promise.all([
        apiService.healthCheck(),
        apiService.getAPIInfo()
      ]);
      
      if (healthResponse.status === 'healthy') {
        setStatus('connected');
        setApiInfo(infoResponse);
      } else {
        setStatus('disconnected');
      }
    } catch (error) {
      setStatus('disconnected');
      console.error('API status check failed:', error);
    }
  };

  useEffect(() => {
    checkAPIStatus();
    // Check every 30 seconds
    const interval = setInterval(checkAPIStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = () => {
    switch (status) {
      case 'connected':
        return <Wifi className="w-4 h-4 text-green-500" />;
      case 'disconnected':
        return <WifiOff className="w-4 h-4 text-red-500" />;
      case 'checking':
        return <AlertCircle className="w-4 h-4 text-yellow-500 animate-pulse" />;
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'connected':
        return 'API Connected';
      case 'disconnected':
        return 'API Disconnected';
      case 'checking':
        return 'Checking...';
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'connected':
        return 'text-green-500';
      case 'disconnected':
        return 'text-red-500';
      case 'checking':
        return 'text-yellow-500';
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50">
      <div className={`bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 flex items-center gap-2 text-sm ${getStatusColor()}`}>
        {getStatusIcon()}
        <span>{getStatusText()}</span>
        {apiInfo && status === 'connected' && (
          <span className="text-gray-400 text-xs">v{apiInfo.version}</span>
        )}
        {status === 'disconnected' && (
          <button
            onClick={checkAPIStatus}
            className="ml-2 text-xs bg-gray-700 hover:bg-gray-600 px-2 py-1 rounded text-white transition-colors"
          >
            Retry
          </button>
        )}
      </div>
      
      {status === 'disconnected' && (
        <div className="mt-2 bg-red-900 border border-red-700 rounded-lg p-3 text-sm text-red-200">
          <p className="font-medium mb-1">Backend Server Not Available</p>
          <p className="text-xs">
            Make sure your FastAPI server is running on http://localhost:8000
          </p>
        </div>
      )}
    </div>
  );
};

export default APIStatus;