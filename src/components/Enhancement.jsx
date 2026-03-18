import React, { useState } from 'react';
import PlayerCard from './PlayerCard';
import { enhancementData, getFailDescription, getEnhancementColor } from '../data/enhancement';

const Enhancement = ({ inventory, money, onEnhance, formatMoney }) => {
  const [selectedCardId, setSelectedCardId] = useState(null);
  const [result, setResult] = useState(null);
  const [isAnimating, setIsAnimating] = useState(false);

  const selectedCard = inventory.find(c => c.id === selectedCardId);
  const enhanceable = inventory.filter(c => c.enhancement < 13);

  const getEnhanceInfo = () => {
    if (!selectedCard) return null;
    return enhancementData[selectedCard.enhancement];
  };

  const handleEnhance = () => {
    if (!selectedCard || isAnimating) return;
    const info = getEnhanceInfo();
    if (!info || money < info.cost) return;

    setIsAnimating(true);
    setResult(null);

    setTimeout(() => {
      const enhanceResult = onEnhance(selectedCardId);
      setResult(enhanceResult);
      setIsAnimating(false);

      if (enhanceResult && enhanceResult.destroyed) {
        setTimeout(() => {
          setSelectedCardId(null);
          setResult(null);
        }, 3000);
      }
    }, 1500);
  };

  const info = getEnhanceInfo();

  const renderEnhancementPanel = () => {
    if (selectedCard) {
      return (
        <>
          <div className={`enhancement-preview ${isAnimating ? 'animating' : ''} ${
            result ? (result.success ? 'success' : result.destroyed ? 'destroyed' : 'failed') : ''
          }`}>
            <PlayerCard card={selectedCard} size="large" />
          </div>

          <div className="enhancement-info">
            <div className="info-grid">
              <div className="info-row">
                <span className="info-label">현재 강화</span>
                <span className="info-value" style={{ color: getEnhancementColor(selectedCard.enhancement) }}>
                  +{selectedCard.enhancement}강
                </span>
              </div>
              <div className="info-row">
                <span className="info-label">목표</span>
                <span className="info-value target">+{selectedCard.enhancement + 1}강</span>
              </div>
              <div className="info-row">
                <span className="info-label">성공 확률</span>
                <span className={`info-value ${info.probability <= 13 ? 'danger' : info.probability <= 30 ? 'warning' : 'safe'}`}>
                  {info.probability}%
                </span>
              </div>
              <div className="info-row">
                <span className="info-label">강화 비용</span>
                <span className="info-value cost">{formatMoney(info.cost)}원</span>
              </div>
              <div className="info-row">
                <span className="info-label">실패 시</span>
                <span className="info-value fail">{getFailDescription(selectedCard.enhancement)}</span>
              </div>
            </div>

            <div className="probability-bar">
              <div
                className="probability-fill"
                style={{
                  width: `${info.probability}%`,
                  background: info.probability <= 13
                    ? 'linear-gradient(90deg, #ff4444, #ff6666)'
                    : info.probability <= 30
                    ? 'linear-gradient(90deg, #ff8800, #ffaa44)'
                    : 'linear-gradient(90deg, #00cc66, #44ff88)',
                }}
              />
              <span className="probability-text">{info.probability}%</span>
            </div>

            <button
              className="btn btn-enhance"
              onClick={handleEnhance}
              disabled={money < info.cost || isAnimating}
            >
              {isAnimating ? '⚡ 강화 중...' : money < info.cost ? '💸 잔액 부족' : '⚡ 강화하기'}
            </button>
          </div>

          {result && (
            <div className={`enhancement-result ${result.success ? 'success' : result.destroyed ? 'destroyed' : 'failed'}`}>
              {result.success ? (
                <p>🎉 강화 성공! +{result.newLevel}강 달성!</p>
              ) : result.destroyed ? (
                <p>💥 선수 카드가 파괴되었습니다!</p>
              ) : (
                <p>❌ 강화 실패! +{result.newLevel}강으로 하락</p>
              )}
            </div>
          )}
        </>
      );
    }

    if (result && result.destroyed) {
      return (
        <div className="destruction-view">
          <div className="destruction-icon">💥</div>
          <p className="destruction-text">선수 카드가 파괴되었습니다!</p>
          <button className="btn btn-secondary" onClick={() => { setResult(null); setSelectedCardId(null); }}>
            확인
          </button>
        </div>
      );
    }

    return (
      <div className="no-selection">
        <div className="no-selection-icon">👈</div>
        <p>왼쪽에서 강화할 선수를 선택하세요</p>
      </div>
    );
  };

  return (
    <div className="enhancement">
      <h2 className="section-title">⚡ 강화</h2>

      <div className="enhancement-layout">
        <div className="enhancement-cards">
          <h3 className="sub-title">강화할 선수 선택</h3>
          {enhanceable.length === 0 ? (
            <div className="empty-state">
              <p>강화 가능한 선수가 없습니다.</p>
              <p className="empty-sub">카드팩을 구매하여 선수를 획득하세요!</p>
            </div>
          ) : (
            <div className="card-grid compact">
              {enhanceable.map(card => (
                <PlayerCard
                  key={card.id}
                  card={card}
                  onClick={() => { if (!isAnimating) { setSelectedCardId(card.id); setResult(null); } }}
                  selected={card.id === selectedCardId}
                  selectable
                  size="small"
                />
              ))}
            </div>
          )}
        </div>

        <div className="enhancement-panel">
          {renderEnhancementPanel()}
        </div>
      </div>
    </div>
  );
};

export default Enhancement;
