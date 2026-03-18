// 강화 데이터: 현재 레벨(인덱스)에서 다음 레벨로 강화 시도 시 정보
// probability: 성공 확률(%)
// cost: 강화 비용(만원)
// failDrop: 실패 시 하락 단계 수
// destroyChance: 실패 시 파괴 확률(%)
export const enhancementData = [
  { targetLevel: 1,  probability: 100, cost: 50,    failDrop: 0, destroyChance: 0  },
  { targetLevel: 2,  probability: 90,  cost: 50,   failDrop: 0, destroyChance: 0  },
  { targetLevel: 3,  probability: 80,  cost: 100,   failDrop: 0, destroyChance: 0  },
  { targetLevel: 4,  probability: 70,  cost: 100,   failDrop: 0, destroyChance: 0  },
  { targetLevel: 5,  probability: 60,  cost: 200,   failDrop: 0, destroyChance: 1  },
  { targetLevel: 6,  probability: 50,  cost: 400,  failDrop: 0, destroyChance: 3  },
  { targetLevel: 7,  probability: 45,  cost: 1000,  failDrop: 0, destroyChance: 5  },
  { targetLevel: 8,  probability: 35,  cost: 1000,  failDrop: 0, destroyChance: 10 },
  { targetLevel: 9,  probability: 30,  cost: 2000,  failDrop: 0, destroyChance: 15 },
  { targetLevel: 10, probability: 25,  cost: 2500, failDrop: 1, destroyChance: 15 },
  { targetLevel: 11, probability: 20,   cost: 2500, failDrop: 1, destroyChance: 20 },
  { targetLevel: 12, probability: 15,   cost: 3000, failDrop: 2, destroyChance: 30 },
  { targetLevel: 13, probability: 10,   cost: 3000, failDrop: 3, destroyChance: 50 },
];

export const getEnhancementColor = (level) => {
  if (level === 0) return '#8892b0';
  if (level <= 3) return '#4CAF50';
  if (level <= 5) return '#2196F3';
  if (level <= 7) return '#9C27B0';
  if (level <= 9) return '#FF5722';
  if (level <= 11) return '#f197cc';
  return '#FFD700';
};

export const getFailDescription = (currentLevel) => {
  const data = enhancementData[currentLevel];
  if (!data) return '';
  if (data.probability === 100) return '실패 없음';

  let desc = '';
  if (data.failDrop === 0) desc = '강화 단계 유지';
  else desc = `${data.failDrop}단계 하락`;

  if (data.destroyChance > 0) {
    desc += ` + 파괴 확률 ${data.destroyChance}%`;
  }
  return desc;
};
