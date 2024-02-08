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

  const renderParagraphs = () => {
    const paragraphs = information.split('<br>');

    return paragraphs.map((paragraph, index) => <p key={index}>{paragraph}</p>);
  };

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
          <div className={styles.tooltiptext}>{renderParagraphs()}</div>
        </div>
      )}
    </div>
  );
};

export default InfoImage;
