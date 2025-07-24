import React from 'react';
import { ArrowRight, Play } from 'lucide-react';

const Hero: React.FC = () => {
  return (
    <section id="home" className="min-h-screen flex items-center justify-center relative overflow-hidden">
      <div className="container mx-auto px-6 text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 fade-in">
            <span className="gradient-text">Transform</span> Your
            <br />
            <span className="text-[#231D54]">Digital Experience</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-600 mb-8 fade-in fade-in-delay-1 leading-relaxed">
            We create stunning, modern solutions that elevate your brand and 
            drive results. Experience the future of digital innovation.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center fade-in fade-in-delay-2">
            <button className="bg-[#231D54] text-white px-8 py-4 rounded-full hover:bg-[#1A153F] transition-all duration-300 hover:scale-105 flex items-center gap-2 pulse-glow">
              Get Started Now
              <ArrowRight size={20} />
            </button>
            
            <button className="glass-effect text-[#231D54] px-8 py-4 rounded-full hover:bg-white hover:shadow-lg transition-all duration-300 flex items-center gap-2">
              <Play size={20} />
              Watch Demo
            </button>
          </div>
          
          <div className="mt-16 fade-in fade-in-delay-3">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-4xl font-bold text-[#231D54] mb-2">500+</div>
                <div className="text-gray-600">Happy Clients</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-[#231D54] mb-2">98%</div>
                <div className="text-gray-600">Success Rate</div>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-[#231D54] mb-2">24/7</div>
                <div className="text-gray-600">Support</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Floating Elements */}
      <div className="absolute top-1/4 left-1/4 w-20 h-20 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full opacity-20 floating"></div>
      <div className="absolute top-1/2 right-1/4 w-16 h-16 bg-gradient-to-br from-blue-400 to-indigo-400 rounded-full opacity-20 floating" style={{animationDelay: '1s'}}></div>
      <div className="absolute bottom-1/4 left-1/2 w-12 h-12 bg-gradient-to-br from-green-400 to-teal-400 rounded-full opacity-20 floating" style={{animationDelay: '2s'}}></div>
    </section>
  );
};

export default Hero;