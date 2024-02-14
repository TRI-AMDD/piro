import TagManager from 'react-gtm-module';
import 'src/global.d';

const tagManagerArgs = { gtmId: 'G-QNR2D22FG3' };

TagManager.initialize(tagManagerArgs);

export const infoHandleHover = (event: string, label: string) => {
  if (window.dataLayer) {
    window.dataLayer.push({
      event: event,
      label: label
    });
  }
};

export const pushEvent = (event: string) => {
  if (window.dataLayer) {
    window.dataLayer.push({
      event: event
    });
  }
};
