import React from 'react';

const TABS = [
  { id: 'shop', label: '카드팩 상점', icon: '🎴' },
  { id: 'inventory', label: '인벤토리', icon: '📦' },
  { id: 'enhance', label: '강화', icon: '⚡' },
  { id: 'exchange', label: '교환 상점', icon: '🔄' },
  { id: 'typing', label: '타자 연습', icon: '⌨️' },
];

const Header = ({ money, formatMoney, activeTab, onTabChange }) => {
  return (
    <header className="header">
      <div className="header-top">
        <h1 className="logo">⚽ FIFA 강화 시뮬레이터</h1>
        <div className="money-display">
          <span className="money-icon">💰</span>
          <span className="money-amount">{formatMoney(money)}원</span>
        </div>
      </div>
      <nav className="tab-nav">
        {TABS.map(tab => (
          <button
            key={tab.id}
            className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => onTabChange(tab.id)}
          >
            <span className="tab-icon">{tab.icon}</span>
            <span className="tab-label">{tab.label}</span>
          </button>
        ))}
      </nav>
    </header>
  );
};

export default Header;
