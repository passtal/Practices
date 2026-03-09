import React, { useState } from 'react';
import './App.css';
import { TOTY_2025_PLAYERS } from './data/players';
import { enhancementData } from './data/enhancement';
import Header from './components/Header';
import Inventory from './components/Inventory';
import CardShop from './components/CardShop';
import Enhancement from './components/Enhancement';
import Exchange from './components/Exchange';
import TypingGame from './components/TypingGame';

const INITIAL_MONEY = 200000; // 만원 단위 (2억)
const PACK_PRICE = 1000;     // 1000만원
const PACK_SIZE = 5;

function App() {
  const [money, setMoney] = useState(INITIAL_MONEY);
  const [inventory, setInventory] = useState([]);
  const [activeTab, setActiveTab] = useState('shop');
  const [nextId, setNextId] = useState(1);

  const formatMoney = (amount) => {
    if (amount >= 10000) {
      const eok = Math.floor(amount / 10000);
      const man = amount % 10000;
      if (man === 0) return `${eok}억`;
      return `${eok}억 ${man.toLocaleString()}만`;
    }
    return `${amount.toLocaleString()}만`;
  };

  const handleBuyPack = () => {
    if (money < PACK_PRICE) return null;

    const newCards = [];
    for (let i = 0; i < PACK_SIZE; i++) {
      const randomPlayer = TOTY_2025_PLAYERS[Math.floor(Math.random() * TOTY_2025_PLAYERS.length)];
      newCards.push({
        id: nextId + i,
        playerId: randomPlayer.id,
        name: randomPlayer.name,
        position: randomPlayer.position,
        ovr: randomPlayer.ovr,
        team: randomPlayer.team,
        enhancement: 0,
      });
    }

    setMoney(m => m - PACK_PRICE);
    setNextId(n => n + PACK_SIZE);
    setInventory(inv => [...inv, ...newCards]);

    return newCards;
  };

  const handleEnhance = (cardId) => {
    const card = inventory.find(c => c.id === cardId);
    if (!card || card.enhancement >= 10) return null;

    const enhanceInfo = enhancementData[card.enhancement];
    if (money < enhanceInfo.cost) return null;

    setMoney(m => m - enhanceInfo.cost);

    const roll = Math.random() * 100;

    if (roll < enhanceInfo.probability) {
      // 성공
      setInventory(inv => inv.map(c =>
        c.id === cardId ? { ...c, enhancement: c.enhancement + 1 } : c
      ));
      return { success: true, newLevel: card.enhancement + 1 };
    } else {
      // 실패 - 파괴 확인
      if (enhanceInfo.destroyChance > 0) {
        const destroyRoll = Math.random() * 100;
        if (destroyRoll < enhanceInfo.destroyChance) {
          // 파괴
          setInventory(inv => inv.filter(c => c.id !== cardId));
          return {
            success: false,
            destroyed: true,
            cardName: card.name,
            cardEnhancement: card.enhancement,
          };
        }
      }
      // 단계 하락
      const newLevel = Math.max(0, card.enhancement - enhanceInfo.failDrop);
      setInventory(inv => inv.map(c =>
        c.id === cardId ? { ...c, enhancement: newLevel } : c
      ));
      return { success: false, destroyed: false, newLevel };
    }
  };

  const handleExchange = (cardIds, desiredPlayerId) => {
    if (cardIds.length !== 3) return false;
    const desiredPlayer = TOTY_2025_PLAYERS.find(p => p.id === desiredPlayerId);
    if (!desiredPlayer) return false;

    // 선택된 카드가 모두 존재하는지 확인
    const allExist = cardIds.every(id => inventory.some(c => c.id === id));
    if (!allExist) return false;

    const newCard = {
      id: nextId,
      playerId: desiredPlayer.id,
      name: desiredPlayer.name,
      position: desiredPlayer.position,
      ovr: desiredPlayer.ovr,
      team: desiredPlayer.team,
      enhancement: 0,
    };

    setInventory(inv => [...inv.filter(c => !cardIds.includes(c.id)), newCard]);
    setNextId(n => n + 1);
    return true;
  };

  const handleTypingComplete = () => {
    setMoney(m => m + INITIAL_MONEY);
  };

  const renderTab = () => {
    switch (activeTab) {
      case 'shop':
        return <CardShop money={money} onBuyPack={handleBuyPack} formatMoney={formatMoney} />;
      case 'inventory':
        return <Inventory inventory={inventory} />;
      case 'enhance':
        return <Enhancement inventory={inventory} money={money} onEnhance={handleEnhance} formatMoney={formatMoney} />;
      case 'exchange':
        return <Exchange inventory={inventory} onExchange={handleExchange} />;
      case 'typing':
        return <TypingGame onComplete={handleTypingComplete} />;
      default:
        return <CardShop money={money} onBuyPack={handleBuyPack} formatMoney={formatMoney} />;
    }
  };

  return (
    <div className="app">
      <Header money={money} formatMoney={formatMoney} activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="main-content">
        {renderTab()}
      </main>
    </div>
  );
}

export default App;
