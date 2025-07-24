import React from 'react';
import { Menu, X } from 'lucide-react';

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass-effect">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="brand-font text-2xl font-bold text-[#231D54]">
            ModernCorp
          </div>
          
          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            <a href="#home" className="text-gray-700 hover:text-[#231D54] transition-colors duration-300">
              Home
            </a>
            <a href="#services" className="text-gray-700 hover:text-[#231D54] transition-colors duration-300">
              Services
            </a>
            <a href="#about" className="text-gray-700 hover:text-[#231D54] transition-colors duration-300">
              About
            </a>
            <a href="#contact" className="text-gray-700 hover:text-[#231D54] transition-colors duration-300">
              Contact
            </a>
          </nav>

          {/* CTA Button */}
          <button className="hidden md:block bg-[#231D54] text-white px-6 py-2 rounded-full hover:bg-[#1A153F] transition-all duration-300 hover:scale-105">
            Get Started
          </button>

          {/* Mobile Menu Button */}
          <button 
            className="md:hidden"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <nav className="md:hidden mt-4 pb-4 glass-effect rounded-lg">
            <div className="flex flex-col space-y-4 px-4">
              <a href="#home" className="text-gray-700 hover:text-[#231D54] transition-colors duration-300">
                Home
              </a>
              <a href="#services" className="text-gray-700 hover:text-[#231D54] transition-colors duration-300">
                Services
              </a>
              <a href="#about" className="text-gray-700 hover:text-[#231D54] transition-colors duration-300">
                About
              </a>
              <a href="#contact" className="text-gray-700 hover:text-[#231D54] transition-colors duration-300">
                Contact
              </a>
              <button className="bg-[#231D54] text-white px-6 py-2 rounded-full hover:bg-[#1A153F] transition-all duration-300 w-full">
                Get Started
              </button>
            </div>
          </nav>
        )}
      </div>
    </header>
  );
};

export default Header;