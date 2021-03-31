from tools import errors

class LawSubject():
    '''Class Description:
    # Args:
        name：民事主体名称
        Civil_Rights_Capacity：民事权利能力
        Civil_Conduct_Capacity：民事行为能力（0：完全民事行为能力；1：限制民事行为能力；2：无民事行为能力）
    # Function:
        information()：返回[type，name, Civil_Conduct_Capacity]
    '''
    def __init__(self, name, Civil_Rights_Capacity=True, Civil_Conduct_Capacity=0):
        
        self.name = name
        self.Civil_Rights_Capacity = Civil_Rights_Capacity
        self.Civil_Conduct_Capacity = Civil_Conduct_Capacity

    def information(self):
        info = [type(self), self.name, self.Civil_Conduct_Capacity]
        return info

    def __repr__(self):
        return self.name
        

class Person(LawSubject):
    '''Class Description:
    Inherted from class LawSubject
    # Args:
        name：民事主体名称
        age：年龄
        gender：性别
        feedself：是否可以以自己劳动收入为主要生活来源
        insane：精神状态（0：正常；1：间歇性；2：完全无法辨认）
        spouse：配偶
        parents：父母列表
        children：子列表
        gardien：监护人
        agent_law：法定代理人
        Civil_Rights_Capacity：民事权利能力
        Civil_Conduct_Capacity：民事行为能力（0：完全民事行为能力；1：限制民事行为能力；2：无民事行为能力）
    # Functions:
        information()：返回[type，name, age, gender, Civil_Conduct_Capacity]
        IsChildof(p)：以p为自己的父/母
        IsParentof(c)：以c为自己的子
    '''
    def __init__(self, name, age, gender, feedself=False, insane=0, 
                spouse=None, parents=[], children=[], 
                gardien=None, agent_law=None, agent_entrusted=None, 
                Civil_Rights_Capacity=True, Civil_Conduct_Capacity=0):
        super().__init__(name, Civil_Rights_Capacity=Civil_Rights_Capacity, Civil_Conduct_Capacity=Civil_Conduct_Capacity)
        self.age = age
        self.gender = gender
        self.insane = insane
        self.feedself = feedself
        if spouse != None:
            self.spouse = spouse
            if self.spouse.spouse == None:
                self.spouse.spouse = self
        else:
            self.spouse = None
        self.parents = []
        self.children = []
        self.parents = self.IsChildof(parents)
        self.children = self.IsParentof(children)
        self.Civil_Conduct_Capacity = self.__conduct_bility(self.age, self.insane, self.feedself)
        if self.Civil_Conduct_Capacity == 0:
            self.gardien = None
            self.agent_law = None
        else:
            self.agent_law = self.__make_agentlaw(agent_law)
            self.gardien = self.agent_law
        self.agent_entrusted = agent_entrusted

    def __conduct_bility(self, age, insane, feedself):
        if insane == 2:
            return 2
        if age >= 18:
            return 0 if insane == 0 else 1
        elif age < 18 and age >= 16:
            return 0 if (feedself and insane == 0) else 1
        elif age >= 8:
            return 1
        else:
            return 2

    def __make_agentlaw(self, agent_law):
        if self.age < 18:
            if self.parents:
                for parent in self.parents:
                    if parent.Civil_Conduct_Capacity == 0:
                        return parent
            # 缺少祖父母为法定代理人的情况
        elif self.age >= 18 and self.insane != 0:
            if self.spouse and self.spouse.Civil_Conduct_Capacity == 0:
                return self.spouse
            elif self.parents:
                for parent in self.parents:
                    if parent.Civil_Conduct_Capacity == 0:
                        return parent
            elif self.children:
                for child in self.children:
                    if child.Civil_Conduct_Capacity == 0:
                        return child
        return agent_law

    def information(self):
        res = [type(self), self.name, self.age, self.gender, self.Civil_Conduct_Capacity]
        return res

    def family_info(self):
        familyinfo = {}
        pptmp = []
        bstmp = []
        cctmp = []
        if self.parents:
            familyinfo['parents'] = self.parents
            for parent in self.parents:
                if parent.parents:
                    pptmp += parent.parents
                if len(parent.children) > 1:
                    bstmp += parent.children
                    bstmp.remove(self)
            if pptmp:
                familyinfo['grandparents'] = list(set(pptmp))
            if bstmp:
                familyinfo['bro_sis'] = list(set(bstmp))
        if self.children:
            familyinfo['children'] = self.children
            for child in self.children:
                if child.children:
                    cctmp += child.children
            if cctmp:
                familyinfo['grandsons'] = list(set(cctmp))
        if self.spouse:
            familyinfo['spouse'] = self.spouse
        return familyinfo


    def IsChildof(self, parents): 
        '''Function Description:
        以parents中的主体为自己的父/母
        '''
        if not parents:
            return []
        for parent in parents:
            if self.age > parent.age:
                raise errors.AgeError('Child is older than parent!')
            self.parents.append(parent)
            if self not in parent.children:
                parent.children.append(self)
        return self.parents

    def IsParentof(self, children): 
        '''Function Description:
        以children中的元素为自己的子
        '''
        if not children:
            return []
        for child in children:
            if self.age < child.age:
                raise errors.AgeError('Parent is younger than child!')
            self.children.append(child)
            if self not in child.parents:
                child.parents.append(self)
        return self.children
   

class LegalPerson(LawSubject):
    '''Class Description:
    Inherted from class LawSubject
    # Args:
        name：民事主体名称
        Civil_Rights_Capacity：民事权利能力
        Civil_Conduct_Capacity：民事行为能力（0：完全民事行为能力；1：限制民事行为能力；2：无民事行为能力）
    # Function:
        information()：返回[type，name, Civil_Conduct_Capacity]
    '''
    def __init__(self, name, Civil_Rights_Capacity=True, Civil_Conduct_Capacity=0):
        super().__init__(name, Civil_Rights_Capacity=Civil_Rights_Capacity, Civil_Conduct_Capacity=Civil_Conduct_Capacity)
        if self.Civil_Rights_Capacity:
            self.Civil_Conduct_Capacity = 0
        

if __name__ == "__main__":
    a = Person('Zahi', 42, 'male')
    b = LegalPerson('Microsoft')
    c = Person('Anny', 40, 'female', insane=2, spouse=a)
    d = Person('Baby', 2, 'male', parents=[c, a])
    e = Person('Wyne', 10, 'female', parents=[c, a])
    person_list = [a, b, c, d, e]
    print(a.children)
    print(c.gardien)
    print(d.parents, d.agent_law, d.gardien)
    print(a.family_info())
    
    

    
