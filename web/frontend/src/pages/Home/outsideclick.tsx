import { useRef, useEffect, useCallback, RefObject } from 'react';

type ClickOutsideHandler = (event: MouseEvent) => void;

export default function useOnClickOutside(handleClickOutside: ClickOutsideHandler): RefObject<HTMLDivElement> {
  const ref = useRef<HTMLDivElement>(null);

  const handleClick = useCallback(
    (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        handleClickOutside(e);
      }
    },
    [handleClickOutside]
  );

  useEffect(() => {
    document.addEventListener('mousedown', handleClick);
    return () => {
      document.removeEventListener('mousedown', handleClick);
    };
  }, [handleClick]);

  return ref;
}
