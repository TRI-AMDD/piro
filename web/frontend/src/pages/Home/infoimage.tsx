import React, { useState } from 'react';
import styles from './tooltip.module.css';

interface InfoImageProps {
  imagePath: string;
  altText: string;
  information: string;
}

const InfoImage: React.FC<InfoImageProps> = ({ imagePath, altText, information }) => {
  const [isTooltipVisible, setTooltipVisible] = useState(false);

  const handleMouseEnter = () => {
    setTooltipVisible(true);
  };

  const handleMouseLeave = () => {
    setTooltipVisible(false);
  };
  const characterToColor: string = '`';
  const lines: string[] = information.split('<br>');
  const modifiedLines: JSX.Element[] = lines.map((line: string, lineIndex: number) => {
    const characters: string[] = line.split('');
    const modifiedCharacters: JSX.Element[] = characters.map((char: string, index: number) => {
      if (char === characterToColor) {
        return (
          <span key={index} style={{ color: '#222020' }}>
            {char}
          </span>
        );
      } else {
        return <span key={index}>{char}</span>;
      }
    });
    const modifiedLine: JSX.Element = <>{modifiedCharacters}</>;
    return <div key={lineIndex}>{modifiedLine}</div>;
  });

  return (
    <div className={styles.container}>
      <img
        src={imagePath}
        alt={altText}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        className={styles.icon}
      />

      {isTooltipVisible && (
        <div className={styles.tooltip}>
          <div className={styles.tooltiptext}>{modifiedLines}</div>
        </div>
      )}
    </div>
  );
};

export default InfoImage;
