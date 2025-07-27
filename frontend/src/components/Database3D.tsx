import { Zap } from "lucide-react";

const Database3D = () => {
  return (
    <div className="relative inline-block">
      <div className="database-3d relative w-32 h-24 mx-auto mb-4">
        <div className="database-layer"></div>
        <div className="database-layer"></div>
        <div className="database-layer"></div>
      </div>
      <div className="absolute -top-2 -right-2">
        <Zap className="w-8 h-8 text-electric-cyan animate-pulse" />
      </div>
    </div>
  );
};

export default Database3D;