import React from 'react';
import { Button } from './ui/button';
import { TrashIcon } from 'lucide-react';

export const DeleteButton = ({ onClick }) => (
  <Button size="icon" variant="ghost" onClick={onClick}>
    <TrashIcon className="w-4 h-4" />
  </Button>
);


