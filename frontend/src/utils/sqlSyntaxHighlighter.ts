interface HighlightToken {
  text: string;
  type: 'keyword' | 'string' | 'number' | 'operator' | 'table' | 'normal';
}

const SQL_KEYWORDS = [
  'SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET',
  'DELETE', 'CREATE', 'TABLE', 'DROP', 'ALTER', 'INDEX', 'SHOW', 'DESCRIBE',
  'AND', 'OR', 'NOT', 'IN', 'LIKE', 'BETWEEN', 'ORDER', 'BY', 'GROUP',
  'HAVING', 'LIMIT', 'OFFSET', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER',
  'UNION', 'ALL', 'DISTINCT', 'AS', 'ON', 'USING', 'CASE', 'WHEN', 'THEN',
  'ELSE', 'END', 'IF', 'NULL', 'TRUE', 'FALSE', 'COUNT', 'SUM', 'AVG',
  'MAX', 'MIN', 'HELP', 'CLEAR', 'EXIT'
];

const TABLE_NAMES = ['users', 'products', 'orders'];

export const tokenizeSQLCommand = (command: string): HighlightToken[] => {
  const tokens: HighlightToken[] = [];
  const regex = /(\s+|[(),;]|'[^']*'|"[^"]*"|[^\s(),;"']+)/g;
  let match;

  while ((match = regex.exec(command)) !== null) {
    const token = match[1];
    
    if (token.trim() === '') {
      tokens.push({ text: token, type: 'normal' });
      continue;
    }

    const upperToken = token.toUpperCase();
    
    if (SQL_KEYWORDS.includes(upperToken)) {
      tokens.push({ text: token, type: 'keyword' });
    } else if (token.match(/^'.*'$/) || token.match(/^".*"$/)) {
      tokens.push({ text: token, type: 'string' });
    } else if (token.match(/^\d+(\.\d+)?$/)) {
      tokens.push({ text: token, type: 'number' });
    } else if (['=', '!=', '<>', '<', '>', '<=', '>=', '+', '-', '*', '/', '%'].includes(token)) {
      tokens.push({ text: token, type: 'operator' });
    } else if (TABLE_NAMES.includes(token.toLowerCase())) {
      tokens.push({ text: token, type: 'table' });
    } else {
      tokens.push({ text: token, type: 'normal' });
    }
  }

  return tokens;
};

export const highlightSQLCommand = (command: string): string => {
  const tokens = tokenizeSQLCommand(command);
  
  return tokens.map(token => {
    switch (token.type) {
      case 'keyword':
        return `<span class="sql-keyword">${token.text}</span>`;
      case 'string':
        return `<span class="sql-string">${token.text}</span>`;
      case 'number':
        return `<span class="sql-number">${token.text}</span>`;
      case 'operator':
        return `<span class="sql-operator">${token.text}</span>`;
      case 'table':
        return `<span class="sql-table">${token.text}</span>`;
      default:
        return token.text;
    }
  }).join('');
};

export const getSQLSuggestions = (input: string): string[] => {
  const words = input.toLowerCase().split(/\s+/);
  const lastWord = words[words.length - 1];
  
  if (!lastWord) return [];
  
  const suggestions: string[] = [];
  
  // Keyword suggestions
  SQL_KEYWORDS.forEach(keyword => {
    if (keyword.toLowerCase().startsWith(lastWord)) {
      suggestions.push(keyword.toLowerCase());
    }
  });
  
  // Table name suggestions
  TABLE_NAMES.forEach(table => {
    if (table.startsWith(lastWord)) {
      suggestions.push(table);
    }
  });
  
  // Common patterns
  if (lastWord.startsWith('sel')) {
    suggestions.push('select * from');
  }
  if (lastWord.startsWith('ins')) {
    suggestions.push('insert into');
  }
  if (lastWord.startsWith('upd')) {
    suggestions.push('update');
  }
  if (lastWord.startsWith('del')) {
    suggestions.push('delete from');
  }
  
  return suggestions.slice(0, 8); // Limit to 8 suggestions
};