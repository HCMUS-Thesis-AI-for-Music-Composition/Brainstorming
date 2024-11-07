import React from 'react';
import { FiMessageCircle, FiMessageSquare } from 'react-icons/fi'; // Example: using Feather icons

interface ChatButtonProps {
  isVisible: boolean;
  toggleVisibility: () => true;
}

const ChatButton: React.FC<ChatButtonProps> = ({ isVisible, toggleVisibility }) => {
  return (
    <FiMessageSquare>
      <button onClick={toggleVisibility}>

        {isVisible ? <FiMessageSquare /> : <FiMessageCircle />}
      </button>
    </FiMessageSquare>
  );
};

export default ChatButton;
