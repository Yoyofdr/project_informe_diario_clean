import React from 'react';
import { Users, Award, Target, TrendingUp } from 'lucide-react';

const About: React.FC = () => {
  return (
    <section id="about" className="py-20 relative">
      <div className="container mx-auto px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-[#231D54]">
              About <span className="gradient-text">Our Company</span>
            </h2>
            <p className="text-lg text-gray-600 mb-8 leading-relaxed">
              We are a team of passionate innovators dedicated to creating exceptional digital experiences. 
              With over a decade of experience, we've helped hundreds of businesses transform their digital presence.
            </p>
            <p className="text-lg text-gray-600 mb-8 leading-relaxed">
              Our mission is to bridge the gap between technology and human connection, creating solutions 
              that not only look beautiful but also deliver meaningful results.
            </p>
            
            <div className="grid grid-cols-2 gap-6">
              <div className="text-center p-4 glass-effect rounded-xl">
                <div className="text-3xl font-bold text-[#231D54] mb-2">10+</div>
                <div className="text-gray-600">Years Experience</div>
              </div>
              <div className="text-center p-4 glass-effect rounded-xl">
                <div className="text-3xl font-bold text-[#231D54] mb-2">500+</div>
                <div className="text-gray-600">Projects Completed</div>
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="glass-effect p-6 rounded-2xl hover-lift text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center text-white mx-auto mb-4">
                <Users size={32} />
              </div>
              <h3 className="text-lg font-semibold mb-2 text-[#231D54]">Expert Team</h3>
              <p className="text-gray-600 text-sm">Skilled professionals with diverse expertise</p>
            </div>
            
            <div className="glass-effect p-6 rounded-2xl hover-lift text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-teal-600 rounded-2xl flex items-center justify-center text-white mx-auto mb-4">
                <Award size={32} />
              </div>
              <h3 className="text-lg font-semibold mb-2 text-[#231D54]">Award Winning</h3>
              <p className="text-gray-600 text-sm">Recognition for excellence in design and development</p>
            </div>
            
            <div className="glass-effect p-6 rounded-2xl hover-lift text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-2xl flex items-center justify-center text-white mx-auto mb-4">
                <Target size={32} />
              </div>
              <h3 className="text-lg font-semibold mb-2 text-[#231D54]">Goal Oriented</h3>
              <p className="text-gray-600 text-sm">Focused on achieving your business objectives</p>
            </div>
            
            <div className="glass-effect p-6 rounded-2xl hover-lift text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-600 rounded-2xl flex items-center justify-center text-white mx-auto mb-4">
                <TrendingUp size={32} />
              </div>
              <h3 className="text-lg font-semibold mb-2 text-[#231D54]">Growth Driven</h3>
              <p className="text-gray-600 text-sm">Strategies that scale with your business</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;