import { TestBed } from '@angular/core/testing';

import { Spendsense } from './spendsense';

describe('Spendsense', () => {
  let service: Spendsense;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Spendsense);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
