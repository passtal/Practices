import React, { useState } from 'react';
import PlayerCard from './PlayerCard';
import { TOTY_2025_PLAYERS } from '../data/players';

const Exchange = ({ inventory, onExchange }) => {
  const [selectedCards, setSelectedCards] = useState([]);
  const [desiredPlayerId, setDesiredPlayerId] = useState(null);
  const [showResult, setShowResult] = useState(false);

  const toggleCard = (cardId) => {
    setSelectedCards(prev => {
      if (prev.includes(cardId)) {
        return prev.filter(id => id !== cardId);
      }
      if (prev.length >= 3) return prev;
      return [...prev, cardId];
    });
  };

  const handleExchange = () => {
    if (selectedCards.length !== 3 || !desiredPlayerId) return;
    const success = onExchange(selectedCards, desiredPlayerId);
    if (success) {
      setShowResult(true);
      setSelectedCards([]);
      setDesiredPlayerId(null);
      setTimeout(() => setShowResult(false), 2500);
    }
  };

  const desiredPlayer = TOTY_2025_PLAYERS.find(p => p.id === desiredPlayerId);

  return (
    <div className="exchange">
      <h2 className="section-title">🔄 교환 상점</h2>
      <p className="exchange-desc">아무 선수 카드 <strong>3장</strong>을 원하는 선수 <strong>1명</strong>으로 확정 교환할 수 있습니다.</p>

      <div className="exchange-layout">
        <div className="exchange-section">
          <h3 className="sub-title">재료 선수 선택 ({selectedCards.length}/3)</h3>
          {inventory.length === 0 ? (
            <div className="empty-state">
              <p>보유한 선수 카드가 없습니다.</p>
            </div>
          ) : inventory.length < 3 ? (
            <div className="empty-state">
              <p>선수 카드가 3장 이상 필요합니다. (현재 {inventory.length}장)</p>
            </div>
          ) : (
            <div className="card-grid compact">
              {inventory.map(card => (
                <PlayerCard
                  key={card.id}
                  card={card}
                  onClick={() => toggleCard(card.id)}
                  selected={selectedCards.includes(card.id)}
                  selectable
                  size="small"
                />
              ))}
            </div>
          )}
        </div>

        <div className="exchange-arrow-container">
          <div className="exchange-arrow">→</div>
        </div>

        <div className="exchange-section">
          <h3 className="sub-title">원하는 선수 선택</h3>
          <div className="desired-player-grid">
            {TOTY_2025_PLAYERS.map(player => (
              <div
                key={player.id}
                className={`desired-player ${desiredPlayerId === player.id ? 'selected' : ''}`}
                onClick={() => setDesiredPlayerId(player.id)}
              >
                <span className="desired-ovr">{player.ovr}</span>
                <span className="desired-name">{player.name}</span>
                <span className="desired-pos">{player.position}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="exchange-summary">
        <div className="summary-materials">
          {selectedCards.length > 0 ? (
            selectedCards.map(id => {
              const card = inventory.find(c => c.id === id);
              return card ? (
                <span key={id} className="summary-chip">{card.name} +{card.enhancement}</span>
              ) : null;
            })
          ) : (
            <span className="summary-placeholder">재료 선수 3명을 선택하세요</span>
          )}
        </div>
        <span className="summary-arrow">→</span>
        <div className="summary-result">
          {desiredPlayer ? (
            <span className="summary-chip gold">{desiredPlayer.name} (OVR {desiredPlayer.ovr})</span>
          ) : (
            <span className="summary-placeholder">원하는 선수를 선택하세요</span>
          )}
        </div>
      </div>

      <button
        className="btn btn-primary btn-lg exchange-btn"
        onClick={handleExchange}
        disabled={selectedCards.length !== 3 || !desiredPlayerId}
      >
        🔄 교환하기
      </button>

      {showResult && (
        <div className="modal-overlay">
          <div className="modal-content exchange-result-modal">
            <h3 className="modal-title">🎉 교환 완료!</h3>
            <p>{desiredPlayer?.name || '선수'} 카드를 획득했습니다!</p>
            <button className="btn btn-gold" onClick={() => setShowResult(false)}>확인</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Exchange;
