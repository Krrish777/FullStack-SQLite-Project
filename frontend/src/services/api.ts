// src/services/api.ts
const API_BASE_URL = 'http://localhost:8000'; // Your FastAPI server URL

// Types matching your FastAPI models
export interface SQLRequest {
  query: string;
  database?: string;
}

export interface SQLResponse {
  success: boolean;
  query: string;
  database: string;
  execution_time_ms: number;
  tokens?: Array<{ type: string; value: string }>;
  parse_tree?: any;
  opcodes?: string[];
  result?: any[];
  message?: string;
  error?: string;
}

export interface DatabaseInfo {
  name: string;
  tables: string[];
}

export interface TableInfo {
  name: string;
  exists: boolean;
}

// API service class
class APIService {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async fetchAPI<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, defaultOptions);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Execute SQL query
  async executeQuery(request: SQLRequest): Promise<SQLResponse> {
    return this.fetchAPI<SQLResponse>('/demo/query', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  // Get all databases
  async getDatabases(): Promise<{ databases: DatabaseInfo[] }> {
    return this.fetchAPI<{ databases: DatabaseInfo[] }>('/demo/databases');
  }

  // Get tables for a specific database
  async getTables(databaseName: string): Promise<{ database: string; tables: string[] }> {
    return this.fetchAPI<{ database: string; tables: string[] }>(`/demo/databases/${databaseName}/tables`);
  }

  // Create a new database
  async createDatabase(databaseName: string): Promise<{ success: boolean; message: string }> {
    return this.fetchAPI<{ success: boolean; message: string }>('/demo/databases', {
      method: 'POST',
      body: JSON.stringify({ name: databaseName }),
    });
  }

  // Delete a database
  async deleteDatabase(databaseName: string): Promise<{ success: boolean; message: string }> {
    return this.fetchAPI<{ success: boolean; message: string }>(`/demo/databases/${databaseName}`, {
      method: 'DELETE',
    });
  }

  // Get table info
  async getTableInfo(tableName: string, database: string = 'main'): Promise<TableInfo> {
    return this.fetchAPI<TableInfo>(`/demo/tables/${tableName}/info?database=${database}`);
  }

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: number }> {
    return this.fetchAPI<{ status: string; timestamp: number }>('/health');
  }

  // Get API info
  async getAPIInfo(): Promise<{ message: string; version: string; author: string; docs: string }> {
    return this.fetchAPI<{ message: string; version: string; author: string; docs: string }>('/');
  }
}

// Export singleton instance
export const apiService = new APIService();
export default apiService;