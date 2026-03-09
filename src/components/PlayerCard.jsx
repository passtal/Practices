import React from 'react';
import { getEnhancementColor } from '../data/enhancement';

const PlayerCard = ({ card, onClick, selected, size = 'normal', selectable = false }) => {
  const enhColor = getEnhancementColor(card.enhancement);
  const cardClass = [
    'player-card',
    size,
    selected ? 'selected' : '',
    selectable ? 'selectable' : '',
    `enhancement-${Math.min(card.enhancement, 10)}`,
  ].filter(Boolean).join(' ');

  return (
    <div className={cardClass} onClick={onClick} style={{ '--enh-color': enhColor }}>
      <div className="card-header">
        <div className="card-ovr">
          <span className="ovr-number">{card.ovr}</span>
          {card.enhancement > 0 && (
            <span className="enhancement-badge" style={{ color: enhColor }}>
              +{card.enhancement}
            </span>
          )}
        </div>
        <div className="card-position">{card.position}</div>
      </div>
      <div className="card-body">
        <div className="card-icon">⚽</div>
      </div>
      <div className="card-footer">
        <div className="card-name">{card.name}</div>
        <div className="card-team">{card.team}</div>
        <div className="card-type">2025 TOTY</div>
      </div>
    </div>
  );
};

export default PlayerCard;
