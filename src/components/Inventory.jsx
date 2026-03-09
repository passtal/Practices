import React, { useState } from 'react';
import PlayerCard from './PlayerCard';

const Inventory = ({ inventory }) => {
  const [sortBy, setSortBy] = useState('ovr');

  const sortedInventory = [...inventory].sort((a, b) => {
    switch (sortBy) {
      case 'ovr':
        return (b.ovr + b.enhancement) - (a.ovr + a.enhancement);
      case 'enhancement':
        return b.enhancement - a.enhancement;
      case 'name':
        return a.name.localeCompare(b.name, 'ko');
      case 'position':
        return a.position.localeCompare(b.position);
      default:
        return 0;
    }
  });

  return (
    <div className="inventory">
      <div className="inventory-header">
        <h2 className="section-title">📦 인벤토리 ({inventory.length}장)</h2>
        <div className="sort-controls">
          <span className="sort-label">정렬:</span>
          {[
            { value: 'ovr', label: 'OVR' },
            { value: 'enhancement', label: '강화' },
            { value: 'name', label: '이름' },
            { value: 'position', label: '포지션' },
          ].map(option => (
            <button
              key={option.value}
              className={`btn btn-sm ${sortBy === option.value ? 'btn-gold' : 'btn-secondary'}`}
              onClick={() => setSortBy(option.value)}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {inventory.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📦</div>
          <p>보유한 선수 카드가 없습니다.</p>
          <p className="empty-sub">카드팩 상점에서 카드팩을 구매해보세요!</p>
        </div>
      ) : (
        <div className="card-grid">
          {sortedInventory.map(card => (
            <PlayerCard key={card.id} card={card} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Inventory;
