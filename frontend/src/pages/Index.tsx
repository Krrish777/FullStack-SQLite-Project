import BackgroundAnimation from "@/components/BackgroundAnimation";
import HeroSection from "@/components/HeroSection";
import FeaturesSection from "@/components/FeaturesSection";
import TechnicalSpecs from "@/components/TechnicalSpecs";
import EducationalFeatures from "@/components/EducationalFeatures";
import Footer from "@/components/Footer";
import ScrollProgress from "@/components/ScrollProgress";

const Index = () => {
  return (
    <div className="min-h-screen bg-background text-foreground relative">
      <ScrollProgress />
      <BackgroundAnimation />
      <HeroSection />
      <FeaturesSection />
      <TechnicalSpecs />
      <EducationalFeatures />
      <Footer />
    </div>
  );
};

export default Index;