// FeedbackButton.tsx

import React from 'react';
import { Button } from '@material-tailwind/react';
import styles from './components.module.css';

interface FeedbackButtonProps {
  showFeedbackButton: boolean;
}

const FeedbackButton: React.FC<FeedbackButtonProps> = () => {
  // Add your feedback button logic here
  return (
    <div className={styles.FeedbackButtonDiv}>
      <Button
        variant="filled"
        size="sm"
        placeholder="Feedback test"
        style={{
          height: '48px',
          width: '104px',
          display: 'inline-flex',
          justifyContent: 'center',
          alignItems: 'center',
          borderRadius: '0px 0px 4px 4px',
          borderTop: '1px solid var(--white, #FFF)',
          borderBottom: '1px solid var(--white, #FFF)',
          borderLeft: '1px solid var(--white, #FFF)',
          background: 'var(--grey-900, #212121)',
          fontSize: '16px',
          fontFamily: 'gellix-medium',
          fontWeight: '500',
          lineHeight: '24px',
          letterSpacing: '0.032px',
          paddingBottom: '12px',
          paddingTop: '12px',
          paddingLeft: '16px',
          paddingRight: '16px'
        }}
        className={`text-center capitalize`}
        onClick={() => window.showCollectorDialog()}
      >
        Feedback
      </Button>
    </div>
  );
};

export default FeedbackButton;
