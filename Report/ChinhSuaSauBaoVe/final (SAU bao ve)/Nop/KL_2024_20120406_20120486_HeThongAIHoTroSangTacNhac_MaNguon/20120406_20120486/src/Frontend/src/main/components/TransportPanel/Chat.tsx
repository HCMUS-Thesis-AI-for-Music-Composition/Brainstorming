import React, { useEffect, useRef, useState } from 'react';

interface ChatProps {
  isVisible: boolean;
  toggleVisibility: () => void;
}

const Chat: React.FC<ChatProps> = ({ isVisible, toggleVisibility }) => {
  const [inputText, setInputText] = useState('');
  const [response, setResponse] = useState('');
  const [messages, setMessages] = useState<string[]>([]);
  const [isHovered, setIsHovered] = useState(false);
  const responses = [
    "Xin chào!",
    "Chúc bạn một ngày tốt lành!",
    "Bạn cần giúp gì không?",
    "Hãy nói cho tôi biết thêm chi tiết.",
    "Rất vui được gặp bạn!",
  ];

  const messageContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Cuộn đến cuối khi có tin nhắn mới
    if (messageContainerRef.current) {
      messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(event.target.value);
  };

  const getRandomResponse = () => {
    const randomIndex = Math.floor(Math.random() * responses.length);
    return responses[randomIndex];
  };

  const handleSubmit = () => {
    // Xử lý ngẫu nhiên một câu trả lời từ mảng các câu trả lời
    const randomResponse = getRandomResponse();
    setResponse(randomResponse);
    setMessages(prevMessages => [...prevMessages, inputText]); // Thêm tin nhắn đã gửi vào danh sách tin nhắn
    setInputText(''); // Xóa trường nhập văn bản sau khi gửi
  };

  const chatStyle: React.CSSProperties = {
    display: isVisible ? 'flex' : 'none',
    flexDirection: 'column',
    position: 'fixed',
    top: '50%',
    right: 0,
    transform: 'translateY(-50%)',
    background: 'linear-gradient(135deg, #f6d365 0%, #fda085 100%)',
    padding: '20px',
    borderRadius: '15px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
    zIndex: 9999,
    width: '300px',
    height: '400px',
    color: '#000',
  };

  const messageContainerStyle: React.CSSProperties = {
    overflowY: 'auto',
    flexGrow: 1,
    color: '#000',
    padding: '10px',
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
    borderRadius: '10px',
    marginBottom: '10px',
  };

  const inputContainerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
  };

  const inputStyle: React.CSSProperties = {
    marginBottom: '10px',
    width: '90%', // Đảm bảo chiều rộng của input không vượt quá khung chat
    padding: '10px',
    borderRadius: '10px',
    border: '1px solid #ccc',
    outline: 'none',
    fontSize: '16px',
  };

  const buttonStyle: React.CSSProperties = {
    width: '90%', // Đảm bảo chiều rộng của nút không vượt quá khung chat
    padding: '10px',
    backgroundColor: isHovered ? '#45a049' : '#4CAF50',
    color: '#fff',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    fontSize: '16px',
    transition: 'background-color 0.3s ease',
  };

  const hideButtonStyle: React.CSSProperties = {
    position: 'absolute',
    top: '10px',
    right: '10px',
    border: 'none',
    background: 'none',
    cursor: 'pointer',
    fontSize: '20px', // Tăng kích thước font cho biểu tượng
    color: '#000', // Đặt màu cho biểu tượng
  };

  return (
    <div style={chatStyle}>
      <button onClick={toggleVisibility} style={hideButtonStyle}>
        &#x2715; {/* Unicode cho biểu tượng "X" */}
      </button>
      {/* Tin nhắn đã nhận */}
      <div style={messageContainerStyle} ref={messageContainerRef}>
        {messages.map((message, index) => (
          <div key={index}>{message}</div>
        ))}
      </div>
      <div style={inputContainerStyle}>
        {/* Input field */}
        <input
          type="text"
          value={inputText}
          onChange={handleInputChange}
          style={inputStyle}
          placeholder="Nhập tin nhắn của bạn..."
        />
        {/* Button to submit text */}
        <button
          onClick={handleSubmit}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          style={buttonStyle}
        >
          Gửi
        </button>
        {/* Display response */}
        <p style={{ color: '#000', marginTop: '10px' }}>{response}</p>
      </div>
    </div>
  );
};

export default Chat;
