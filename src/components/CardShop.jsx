import React, { useState } from 'react';
import PlayerCard from './PlayerCard';

const PACK_PRICE = 1000;

const CardShop = ({ money, onBuyPack, formatMoney }) => {
  const [packResult, setPackResult] = useState(null);
  const [isOpening, setIsOpening] = useState(false);

  const handleBuy = () => {
    if (money < PACK_PRICE || isOpening) return;
    setIsOpening(true);

    setTimeout(() => {
      const cards = onBuyPack();
      setPackResult(cards);
      setIsOpening(false);
    }, 800);
  };

  const closePack = () => {
    setPackResult(null);
  };

  return (
    <div className="card-shop">
      <h2 className="section-title">🎴 카드팩 상점</h2>

      <div className="pack-container">
        <div className={`card-pack ${isOpening ? 'opening' : ''}`}>
          <div className="pack-design">
            <div className="pack-stars">★ ★ ★</div>
            <div className="pack-logo">2025</div>
            <div className="pack-title">TOTY</div>
            <div className="pack-subtitle">TEAM OF THE YEAR</div>
            <div className="pack-count">× 5 Players</div>
            <div className="pack-stars">★ ★ ★</div>
          </div>
        </div>

        <div className="pack-info">
          <h3>2025 TOTY 카드팩</h3>
          <p className="pack-desc">2025 TOTY 선수 중 랜덤 5명이 지급됩니다.</p>
          <p className="pack-price">가격: <strong>{formatMoney(PACK_PRICE)}원</strong></p>
          <p className="pack-balance">보유 금액: <strong>{formatMoney(money)}원</strong></p>
          <button
            className="btn btn-primary btn-lg"
            onClick={handleBuy}
            disabled={money < PACK_PRICE || isOpening}
          >
            {isOpening ? '개봉 중...' : money < PACK_PRICE ? '💸 잔액 부족' : '🎴 구매하기'}
          </button>
        </div>
      </div>

      {packResult && (
        <div className="modal-overlay" onClick={closePack}>
          <div className="modal-content pack-result" onClick={e => e.stopPropagation()}>
            <h3 className="modal-title">🎉 카드팩 개봉 결과!</h3>
            <div className="pack-cards">
              {packResult.map((card, index) => (
                <div
                  key={card.id}
                  className="pack-card-reveal"
                  style={{ animationDelay: `${index * 0.15}s` }}
                >
                  <PlayerCard card={card} size="small" />
                </div>
              ))}
            </div>
            <button className="btn btn-gold" onClick={closePack}>확인</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default CardShop;
