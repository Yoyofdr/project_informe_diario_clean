import React from 'react';
import { Heart } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-[#231D54] text-white py-12">
      <div className="container mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="brand-font text-2xl font-bold mb-4">
              ModernCorp
            </div>
            <p className="text-gray-300 leading-relaxed">
              Creating exceptional digital experiences that drive results and inspire innovation.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Services</h3>
            <ul className="space-y-2 text-gray-300">
              <li><a href="#" className="hover:text-white transition-colors">Web Development</a></li>
              <li><a href="#" className="hover:text-white transition-colors">UI/UX Design</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Mobile Apps</a></li>
              <li><a href="#" className="hover:text-white transition-colors">SEO & Marketing</a></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Company</h3>
            <ul className="space-y-2 text-gray-300">
              <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Our Team</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact</h3>
            <ul className="space-y-2 text-gray-300">
              <li>hello@moderncorp.com</li>
              <li>+1 (555) 123-4567</li>
              <li>123 Innovation Street<br />Tech City, TC 12345</li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-600 mt-8 pt-8 text-center text-gray-300">
          <p className="flex items-center justify-center gap-2">
            Made with <Heart size={16} className="text-red-500" /> by ModernCorp
          </p>
          <p className="mt-2">© 2024 ModernCorp. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;