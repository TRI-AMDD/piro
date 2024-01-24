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
        size="md"
        placeholder="Feedback"
        style={{ fontSize: '15px', fontFamily: 'gellix-regular' }}
        className={`${styles.FeedbackButton} text-center capitalize`}
        onClick={() => window.showCollectorDialog()}
      >
        Feedback
      </Button>
    </div>
  );
};

export default FeedbackButton;
