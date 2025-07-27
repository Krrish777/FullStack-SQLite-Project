const BackgroundAnimation = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none" style={{ zIndex: -1 }}>
      {/* Floating gradient circles with very low opacity */}
      <div 
        className="absolute w-96 h-96 rounded-full floating opacity-5"
        style={{
          background: 'radial-gradient(circle, hsl(200 100% 60%) 0%, transparent 70%)',
          top: '10%',
          left: '10%',
        }}
      />
      <div 
        className="absolute w-80 h-80 rounded-full floating-delayed opacity-5"
        style={{
          background: 'radial-gradient(circle, hsl(170 100% 50%) 0%, transparent 70%)',
          top: '60%',
          right: '15%',
        }}
      />
      <div 
        className="absolute w-64 h-64 rounded-full floating-slow opacity-5"
        style={{
          background: 'radial-gradient(circle, hsl(210 100% 55%) 0%, transparent 70%)',
          bottom: '20%',
          left: '20%',
        }}
      />
      <div 
        className="absolute w-72 h-72 rounded-full floating opacity-5"
        style={{
          background: 'radial-gradient(circle, hsl(180 100% 50%) 0%, transparent 70%)',
          top: '30%',
          right: '40%',
        }}
      />
    </div>
  );
};

export default BackgroundAnimation;