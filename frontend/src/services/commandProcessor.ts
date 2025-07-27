// src/services/commandProcessor.ts
import { apiService, SQLResponse } from './api';

export interface CommandResult {
  success: boolean;
  message?: string;
  data?: any;
  error?: string;
  execution_time_ms?: number;
  type: 'dot-command' | 'sql-query';
}

export class CommandProcessor {
  private currentDatabase: string = 'main';

  constructor() {
    this.currentDatabase = 'main';
  }

  // Get current database
  getCurrentDatabase(): string {
    return this.currentDatabase;
  }

  // Set current database
  setCurrentDatabase(dbName: string): void {
    this.currentDatabase = dbName;
  }

  // Main command processing function
  async processCommand(command: string): Promise<CommandResult> {
    const trimmedCommand = command.trim();
    
    if (!trimmedCommand) {
      return {
        success: false,
        error: 'Empty command',
        type: 'dot-command'
      };
    }

    const startTime = Date.now();

    try {
      // Check if it's a dot command
      if (trimmedCommand.startsWith('.')) {
        return await this.processDotCommand(trimmedCommand, startTime);
      } else {
        // It's a SQL query
        return await this.processSQLQuery(trimmedCommand, startTime);
      }
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
        execution_time_ms: Date.now() - startTime,
        type: trimmedCommand.startsWith('.') ? 'dot-command' : 'sql-query'
      };
    }
  }

  // Process dot commands
  private async processDotCommand(command: string, startTime: number): Promise<CommandResult> {
    const parts = command.split(/\s+/);
    const dotCommand = parts[0];

    switch (dotCommand) {
      case '.create-db':
        if (parts.length < 2) {
          return {
            success: false,
            error: 'Usage: .create-db <database_name>',
            execution_time_ms: Date.now() - startTime,
            type: 'dot-command'
          };
        }
        return await this.createDatabase(parts[1], startTime);

      case '.list-dbs':
        return await this.listDatabases(startTime);

      case '.use-db':
        if (parts.length < 2) {
          return {
            success: false,
            error: 'Usage: .use-db <database_name>',
            execution_time_ms: Date.now() - startTime,
            type: 'dot-command'
          };
        }
        return await this.useDatabase(parts[1], startTime);

      case '.show-tables':
        return await this.showTables(startTime);

      case '.drop-db':
        if (parts.length < 2) {
          return {
            success: false,
            error: 'Usage: .drop-db <database_name>',
            execution_time_ms: Date.now() - startTime,
            type: 'dot-command'
          };
        }
        return await this.dropDatabase(parts[1], startTime);

      case '.help':
        return this.showHelp(startTime);

      case '.exit':
        return {
          success: true,
          message: 'Goodbye!',
          execution_time_ms: Date.now() - startTime,
          type: 'dot-command',
          data: { action: 'exit' }
        };

      default:
        return {
          success: false,
          error: `Unknown dot command: ${dotCommand}. Type .help for available commands.`,
          execution_time_ms: Date.now() - startTime,
          type: 'dot-command'
        };
    }
  }

  // Process SQL queries
  private async processSQLQuery(query: string, startTime: number): Promise<CommandResult> {
    try {
      const response: SQLResponse = await apiService.executeQuery({
        query: query,
        database: this.currentDatabase
      });

      return {
        success: response.success,
        message: response.message,
        error: response.error,
        execution_time_ms: response.execution_time_ms,
        type: 'sql-query',
        data: {
          tokens: response.tokens,
          parse_tree: response.parse_tree,
          opcodes: response.opcodes,
          result: response.result,
          query: response.query,
          database: response.database
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to execute SQL query',
        execution_time_ms: Date.now() - startTime,
        type: 'sql-query'
      };
    }
  }

  // Individual dot command handlers
  private async createDatabase(dbName: string, startTime: number): Promise<CommandResult> {
    try {
      const response = await apiService.createDatabase(dbName);
      return {
        success: response.success,
        message: response.message,
        execution_time_ms: Date.now() - startTime,
        type: 'dot-command',
        data: { database: dbName, action: 'create' }
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to create database',
        execution_time_ms: Date.now() - startTime,
        type: 'dot-command'
      };
    }
  }

  private async listDatabases(startTime: number): Promise<CommandResult> {
    try {
      const response = await apiService.getDatabases();
      const dbList = response.databases.map(db => `${db.name} (${db.tables.length} tables)`).join('\n');
      
      return {
        success: true,
        message: `Available databases:\n${dbList}`,
        execution_time_ms: Date.now() - startTime,
        type: 'dot-command',
        data: { databases: response.databases, action: 'list' }
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to list databases',
        execution_time_ms: Date.now() - startTime,
        type: 'dot-command'
      };
    }
  }

  private async useDatabase(dbName: string, startTime: number): Promise<CommandResult> {
    try {
      // First check if database exists
      const response = await apiService.getDatabases();
      const dbExists = response.databases.some(db => db.name === dbName);
      
      if (!dbExists) {
        return {
          success: false,
          error: `Database '${dbName}' does not exist. Use .list-dbs to see available databases.`,
          execution_time_ms: Date.now() - startTime,
          type: 'dot-command'
        };
      }

      // Switch to the database
      this.currentDatabase = dbName;
      
      return {
        success: true,
        message: `Switched to database '${dbName}'`,
        execution_time_ms: Date.now() - startTime,
        type: 'dot-command',
        data: { database: dbName, action: 'switch' }
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to switch database',
        execution_time_ms: Date.now() - startTime,
        type: 'dot-command'
      };
    }
  }

  private async showTables(startTime: number): Promise<CommandResult> {
    try {
      const response = await apiService.getTables(this.currentDatabase);
      const tableList = response.tables.length > 0 
        ? response.tables.join('\n') 
        : 'No tables found in this database';
      
      return {
        success: true,
        message: `Tables in database '${this.currentDatabase}':\n${tableList}`,
        execution_time_ms: Date.now() - startTime,
        type: 'dot-command',
        data: { tables: response.tables, database: this.currentDatabase, action: 'show-tables' }
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to show tables',
        execution_time_ms: Date.now() - startTime,
        type: 'dot-command'
      };
    }
  }

  private async dropDatabase(dbName: string, startTime: number): Promise<CommandResult> {
    try {
      const response = await apiService.deleteDatabase(dbName);
      
      // If we deleted the current database, switch to main
      if (this.currentDatabase === dbName) {
        this.currentDatabase = 'main';
      }
      
      return {
        success: response.success,
        message: response.message + (this.currentDatabase === 'main' ? ' Switched to main database.' : ''),
        execution_time_ms: Date.now() - startTime,
        type: 'dot-command',
        data: { database: dbName, action: 'drop', currentDatabase: this.currentDatabase }
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to drop database',
        execution_time_ms: Date.now() - startTime,
        type: 'dot-command'
      };
    }
  }

  private showHelp(startTime: number): CommandResult {
    const helpText = `
Available Commands:

Database Management:
  .create-db <name>     - Create a new database
  .list-dbs            - List all databases
  .use-db <name>       - Switch to a database
  .drop-db <name>      - Delete a database
  .show-tables         - Show tables in current database

SQL Operations:
  CREATE TABLE ...     - Create a new table
  INSERT INTO ...      - Insert data into table
  SELECT ...           - Query data from table
  UPDATE ...           - Update existing data
  DELETE FROM ...      - Delete data from table
  DROP TABLE ...       - Delete a table

General:
  .help               - Show this help message
  .exit               - Exit the application

Current database: ${this.currentDatabase}
    `;

    return {
      success: true,
      message: helpText.trim(),
      execution_time_ms: Date.now() - startTime,
      type: 'dot-command',
      data: { action: 'help', currentDatabase: this.currentDatabase }
    };
  }
}

// Export singleton instance
export const commandProcessor = new CommandProcessor();
export default commandProcessor;