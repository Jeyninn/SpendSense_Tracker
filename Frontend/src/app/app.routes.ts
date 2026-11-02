import { Routes } from '@angular/router';
import { Dashboard } from './components/dashboard/dashboard';
import { ExpenseForm } from './components/expense-form/expense-form';
import { ExpenseList } from './components/expense-list/expense-list';
import { Signup } from './components/signup/signup';
import { Login } from './components/login/login';
import { Profile } from './components/profile/profile';
import { Home } from './components/home/home';
import { AppLayout } from './components/layout/app-layout/app-layout';
import { IncomeForm } from './components/income-form/income-form';
import { authGuard } from './guards/auth.guard';
import { SpendSense } from './components/spendsense/spendsense';
export const routes: Routes = [
  {
    path: '',
    component: Home,
    pathMatch: 'full'
  },
   { path: 'login', component: Login },
  { path: 'signup', component: Signup },


  {
    path: '',
    component: AppLayout,
    canActivate: [authGuard],

    children: [
      {
        path: 'dashboard',
        component: Dashboard,

      },
      {
        path: 'expenseform',
        component: ExpenseForm
      },
      {
        path: 'expenselist',
        component: ExpenseList
      },
      {
        path: 'profile',
        component: Profile
      },
      { path: 'incomeform', component: IncomeForm },
      {
        path: 'spendsense',
        component: SpendSense
      },

    ]
  },

  {
    path: '**',
    redirectTo: ''
  }
];
