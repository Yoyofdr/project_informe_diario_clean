import React from 'react';
import { Code, Palette, Zap, Shield, Globe, Smartphone } from 'lucide-react';

const Services: React.FC = () => {
  const services = [
    {
      icon: <Code size={40} />,
      title: 'Web Development',
      description: 'Custom web applications built with modern technologies and best practices.',
      gradient: 'from-blue-500 to-indigo-600'
    },
    {
      icon: <Palette size={40} />,
      title: 'UI/UX Design',
      description: 'Beautiful, intuitive designs that enhance user experience and engagement.',
      gradient: 'from-purple-500 to-pink-600'
    },
    {
      icon: <Smartphone size={40} />,
      title: 'Mobile Apps',
      description: 'Native and cross-platform mobile applications for iOS and Android.',
      gradient: 'from-green-500 to-teal-600'
    },
    {
      icon: <Zap size={40} />,
      title: 'Performance',
      description: 'Lightning-fast applications optimized for speed and performance.',
      gradient: 'from-yellow-500 to-orange-600'
    },
    {
      icon: <Shield size={40} />,
      title: 'Security',
      description: 'Enterprise-grade security measures to protect your data and users.',
      gradient: 'from-red-500 to-rose-600'
    },
    {
      icon: <Globe size={40} />,
      title: 'SEO & Marketing',
      description: 'Comprehensive digital marketing strategies to grow your online presence.',
      gradient: 'from-indigo-500 to-purple-600'
    }
  ];

  return (
    <section id="services" className="py-20 relative">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-[#231D54]">
            Our Services
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            We offer comprehensive digital solutions to help your business thrive in the modern world.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <div
              key={index}
              className="glass-effect p-8 rounded-2xl hover-lift group cursor-pointer"
            >
              <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${service.gradient} flex items-center justify-center text-white mb-6 group-hover:scale-110 transition-transform duration-300`}>
                {service.icon}
              </div>
              <h3 className="text-xl font-semibold mb-4 text-[#231D54]">
                {service.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {service.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Services;