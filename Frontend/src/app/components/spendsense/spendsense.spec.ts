import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Spendsense } from './spendsense';

describe('Spendsense', () => {
  let component: Spendsense;
  let fixture: ComponentFixture<Spendsense>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Spendsense],
    }).compileComponents();

    fixture = TestBed.createComponent(Spendsense);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
