import { useCallback, useState } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  MarkerType,
  Node,
  Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Database, RefreshCw } from "lucide-react";

const initialNodes: Node[] = [
  {
    id: 'users',
    type: 'default',
    position: { x: 50, y: 50 },
    data: { 
      label: (
        <div className="p-3">
          <div className="font-bold text-primary mb-2 border-b border-border pb-1">users</div>
          <div className="text-xs space-y-1 text-left">
            <div className="font-semibold text-primary">🔑 id: INTEGER (PK)</div>
            <div>name: TEXT</div>
            <div>email: TEXT UNIQUE</div>
            <div>created_at: TIMESTAMP</div>
          </div>
        </div>
      )
    },
    style: { 
      width: 200, 
      height: 130, 
      background: 'hsl(var(--card))', 
      border: '2px solid hsl(var(--primary))',
      borderRadius: '8px',
      fontSize: '12px'
    }
  },
  {
    id: 'posts',
    type: 'default',
    position: { x: 350, y: 50 },
    data: { 
      label: (
        <div className="p-3">
          <div className="font-bold text-primary mb-2 border-b border-border pb-1">posts</div>
          <div className="text-xs space-y-1 text-left">
            <div className="font-semibold text-primary">🔑 id: INTEGER (PK)</div>
            <div className="text-orange-500">🔗 user_id: INTEGER (FK)</div>
            <div>title: TEXT</div>
            <div>content: TEXT</div>
            <div>created_at: TIMESTAMP</div>
          </div>
        </div>
      )
    },
    style: { 
      width: 200, 
      height: 150, 
      background: 'hsl(var(--card))', 
      border: '2px solid hsl(var(--primary))',
      borderRadius: '8px',
      fontSize: '12px'
    }
  },
  {
    id: 'comments',
    type: 'default',
    position: { x: 200, y: 280 },
    data: { 
      label: (
        <div className="p-3">
          <div className="font-bold text-primary mb-2 border-b border-border pb-1">comments</div>
          <div className="text-xs space-y-1 text-left">
            <div className="font-semibold text-primary">🔑 id: INTEGER (PK)</div>
            <div className="text-orange-500">🔗 post_id: INTEGER (FK)</div>
            <div className="text-orange-500">🔗 user_id: INTEGER (FK)</div>
            <div>content: TEXT</div>
            <div>created_at: TIMESTAMP</div>
          </div>
        </div>
      )
    },
    style: { 
      width: 200, 
      height: 150, 
      background: 'hsl(var(--card))', 
      border: '2px solid hsl(var(--primary))',
      borderRadius: '8px',
      fontSize: '12px'
    }
  }
];

const initialEdges: Edge[] = [
  {
    id: 'users-posts',
    source: 'users',
    target: 'posts',
    type: 'smoothstep',
    label: '1:N',
    labelStyle: { fill: 'hsl(var(--primary))', fontWeight: 600, fontSize: 12 },
    style: { stroke: 'hsl(var(--primary))', strokeWidth: 3 },
    markerEnd: { type: MarkerType.ArrowClosed, color: 'hsl(var(--primary))' }
  },
  {
    id: 'users-comments',
    source: 'users',
    target: 'comments',
    type: 'smoothstep',
    label: '1:N',
    labelStyle: { fill: 'hsl(var(--primary))', fontWeight: 600, fontSize: 12 },
    style: { stroke: 'hsl(var(--primary))', strokeWidth: 3 },
    markerEnd: { type: MarkerType.ArrowClosed, color: 'hsl(var(--primary))' }
  },
  {
    id: 'posts-comments',
    source: 'posts',
    target: 'comments',
    type: 'smoothstep',
    label: '1:N',
    labelStyle: { fill: 'hsl(var(--primary))', fontWeight: 600, fontSize: 12 },
    style: { stroke: 'hsl(var(--primary))', strokeWidth: 3 },
    markerEnd: { type: MarkerType.ArrowClosed, color: 'hsl(var(--primary))' }
  }
];

const DatabaseSchemaVisualizer = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  const resetLayout = () => {
    setNodes(initialNodes);
    setEdges(initialEdges);
  };

  return (
    <Card className="feature-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Database className="w-5 h-5 text-primary" />
          Database Schema Visualizer
        </CardTitle>
        <div className="flex justify-between items-center">
          <p className="text-sm text-muted-foreground">
            Interactive diagram showing table relationships and foreign keys
          </p>
          <Button variant="outline" size="sm" onClick={resetLayout}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Reset
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="h-[400px] w-full border border-border rounded-lg overflow-hidden">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            fitView
            style={{ background: 'hsl(var(--background))' }}
            nodesDraggable={true}
            nodesConnectable={false}
            elementsSelectable={true}
            connectionLineStyle={{ stroke: 'hsl(var(--primary))', strokeWidth: 3 }}
            defaultEdgeOptions={{ 
              style: { stroke: 'hsl(var(--primary))', strokeWidth: 3 },
              markerEnd: { type: MarkerType.ArrowClosed, color: 'hsl(var(--primary))' }
            }}
          >
            <Controls />
            <Background color="hsl(var(--muted))" />
            <MiniMap 
              style={{ background: 'hsl(var(--muted))' }}
              maskColor="hsl(var(--background) / 0.8)"
              nodeColor="hsl(var(--primary))"
            />
          </ReactFlow>
        </div>
        <div className="mt-4 text-xs text-muted-foreground">
          <p>• Drag nodes to rearrange • Zoom and pan to explore • PK = Primary Key, FK = Foreign Key</p>
        </div>
      </CardContent>
    </Card>
  );
};

export default DatabaseSchemaVisualizer;