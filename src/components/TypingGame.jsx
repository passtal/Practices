import React, { useState, useRef, useEffect } from 'react';
import { ANTHEM_LINES, ANTHEM_SECTIONS } from '../data/anthem';

const TypingGame = ({ onComplete }) => {
  const [currentLine, setCurrentLine] = useState(0);
  const [input, setInput] = useState('');
  const [isComplete, setIsComplete] = useState(false);
  const [isStarted, setIsStarted] = useState(false);
  const [completedLines, setCompletedLines] = useState(0);
  const inputRef = useRef(null);

  useEffect(() => {
    if (isStarted && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isStarted, currentLine]);

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInput(value);

    if (value === ANTHEM_LINES[currentLine]) {
      if (currentLine < ANTHEM_LINES.length - 1) {
        setTimeout(() => {
          setCurrentLine(prev => prev + 1);
          setCompletedLines(prev => prev + 1);
          setInput('');
        }, 300);
      } else {
        setIsComplete(true);
        setCompletedLines(ANTHEM_LINES.length);
        onComplete();
      }
    }
  };

  const handleReset = () => {
    setIsStarted(false);
    setIsComplete(false);
    setCurrentLine(0);
    setInput('');
    setCompletedLines(0);
  };

  const getCurrentSection = () => {
    return ANTHEM_SECTIONS.find(s => currentLine >= s.startLine && currentLine <= s.endLine);
  };

  const progress = (completedLines / ANTHEM_LINES.length) * 100;

  if (!isStarted) {
    return (
      <div className="typing-game">
        <h2 className="section-title">⌨️ 타자 연습</h2>
        <div className="typing-intro">
          <div className="typing-intro-icon">🇰🇷</div>
          <h3>애국가 타자 연습</h3>
          <p>애국가 1절부터 4절까지 후렴 포함 정확하게 타이핑하면</p>
          <p className="typing-reward"><strong>2억원</strong>을 지급받습니다!</p>
          <div className="typing-rules">
            <p>• 화면에 표시된 텍스트를 정확히 입력하세요</p>
            <p>• 한 줄을 완성하면 자동으로 다음 줄로 넘어갑니다</p>
            <p>• 총 {ANTHEM_LINES.length}줄을 완성해야 합니다</p>
          </div>
          <button className="btn btn-primary btn-lg" onClick={() => setIsStarted(true)}>
            🎵 시작하기
          </button>
        </div>
      </div>
    );
  }

  if (isComplete) {
    return (
      <div className="typing-game">
        <h2 className="section-title">⌨️ 타자 연습</h2>
        <div className="typing-complete">
          <div className="complete-icon">🎉</div>
          <h3>축하합니다!</h3>
          <p>애국가 4절까지 모두 완료했습니다!</p>
          <p className="typing-reward"><strong>2억원</strong>이 지급되었습니다!</p>
          <button className="btn btn-primary btn-lg" onClick={handleReset}>
            다시 하기
          </button>
        </div>
      </div>
    );
  }

  const section = getCurrentSection();
  const targetLine = ANTHEM_LINES[currentLine];

  return (
    <div className="typing-game">
      <h2 className="section-title">⌨️ 타자 연습 - 애국가</h2>

      <div className="typing-progress">
        <div className="progress-bar-container">
          <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
        </div>
        <span className="progress-text">{completedLines}/{ANTHEM_LINES.length} 줄 완료</span>
      </div>

      <div className="typing-section-badge">{section?.title} {currentLine <= 1 || (currentLine >= 4 && currentLine <= 5) || (currentLine >= 8 && currentLine <= 9) || (currentLine >= 12 && currentLine <= 13) ? '' : '(후렴)'}</div>

      <div className="typing-area">
        <div className="target-text">
          {targetLine.split('').map((char, i) => {
            let className = 'target-char';
            if (i < input.length) {
              className += input[i] === char ? ' correct' : ' incorrect';
            } else if (i === input.length) {
              className += ' current';
            }
            return <span key={i} className={className}>{char}</span>;
          })}
        </div>

        <input
          ref={inputRef}
          type="text"
          className="typing-input"
          value={input}
          onChange={handleInputChange}
          placeholder="위의 텍스트를 입력하세요..."
          autoComplete="off"
          autoCorrect="off"
          spellCheck="false"
        />
      </div>

      <div className="anthem-preview">
        <h4>전체 가사</h4>
        {ANTHEM_SECTIONS.map(section => (
          <div key={section.title} className="anthem-section">
            <div className="anthem-section-title">{section.title}</div>
            {ANTHEM_LINES.slice(section.startLine, section.endLine + 1).map((line, i) => {
              const lineIndex = section.startLine + i;
              return (
                <div
                  key={lineIndex}
                  className={`anthem-line ${lineIndex < currentLine ? 'completed' : lineIndex === currentLine ? 'current' : 'pending'}`}
                >
                  {lineIndex < currentLine ? '✅ ' : lineIndex === currentLine ? '👉 ' : '　 '}
                  {line}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TypingGame;
