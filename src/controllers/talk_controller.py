from fastapi.responses import JSONResponse
aphro={
  "god": "Aphrodite",
  "god_message": "Ah, a mortal dares to enter my realm of eternal beauty. Speak, and make your intentions known.",
  "choice_1": {
    "choice_description": "Compliment Aphrodite's unparalleled beauty.",
    "god_message": "Flattery is appreciated, yet it is but a small gesture. What more do you offer?",
    "choice_score": "good",
    "choice_1": {
      "choice_description": "Offer a rare flower that symbolizes eternal beauty.",
      "god_message": "A fitting gift for a goddess, yet my aid is not so easily won. I shall consider your request.",
      "choice_score": "good",
      "choice_1": {
        "choice_description": "Pledge to spread tales of Aphrodite's beauty across the lands.",
        "god_message": "Your words are sweet, but I need time to ponder. Return to your world, mortal.",
        "choice_score": "good"
      },
      "choice_2": {
        "choice_description": "Promise to build a temple in her honor.",
        "god_message": "Many temples stand in my name already. I shall think on your offer.",
        "choice_score": "neutral"
      },
      "choice_3": {
        "choice_description": "Vow to dedicate your victory in war to her.",
        "god_message": "War and love are strange bedfellows, but I shall consider your proposition.",
        "choice_score": "bad"
      }
    },
    "choice_2": {
      "choice_description": "Recite a poem in her honor.",
      "god_message": "A sweet melody of words, but what actions will follow this?",
      "choice_score": "neutral",
      "choice_1": {
        "choice_description": "Offer to compose a grand epic about her.",
        "god_message": "An epic for the ages... Intriguing. I will think on this.",
        "choice_score": "good"
      },
      "choice_2": {
        "choice_description": "Suggest a festival in her name to celebrate love.",
        "god_message": "Festivals are common, yet I am tempted. I will consider.",
        "choice_score": "neutral"
      },
      "choice_3": {
        "choice_description": "Propose an alliance against her rivals.",
        "god_message": "Intrigue and alliances? A dangerous path. I need time to decide.",
        "choice_score": "bad"
      }
    },
    "choice_3": {
      "choice_description": "Present a handcrafted golden necklace.",
      "god_message": "A token of your esteem, yet what does it truly signify?",
      "choice_score": "bad",
      "choice_1": {
        "choice_description": "Declare it symbolizes your undying devotion.",
        "god_message": "Devotion is a strong vow. I will take time to ponder your words.",
        "choice_score": "good"
      },
      "choice_2": {
        "choice_description": "Explain it represents the beauty and wealth you can offer.",
        "god_message": "Material wealth holds little sway over me. I shall think on it.",
        "choice_score": "neutral"
      },
      "choice_3": {
        "choice_description": "Suggest it will enhance her already stunning appearance.",
        "god_message": "Flattery again? I must contemplate your true intentions.",
        "choice_score": "bad"
      }
    }
  },
  "choice_2": {
    "choice_description": "Ask for her assistance in winning the heart of a loved one.",
    "god_message": "Love is my domain, but why should I meddle in mortal affairs?",
    "choice_score": "neutral",
    "choice_1": {
      "choice_description": "Promise to dedicate a victory in her name if she assists.",
      "god_message": "Victory in love or war? A complex offer, but I will think on it.",
      "choice_score": "good",
      "choice_1": {
        "choice_description": "Assure her of spreading her worship through this love story.",
        "god_message": "A tale of love to inspire devotion... I will consider your words.",
        "choice_score": "good"
      },
      "choice_2": {
        "choice_description": "Offer a sacrifice in her temple.",
        "god_message": "Sacrifices are customary. I shall take time to decide.",
        "choice_score": "neutral"
      },
      "choice_3": {
        "choice_description": "Suggest that your union will be a symbol of her power.",
        "god_message": "Power in love is intriguing, yet I must ponder this further.",
        "choice_score": "bad"
      }
    },
    "choice_2": {
      "choice_description": "Plead for her mercy and understanding.",
      "god_message": "Compassion can be found in my realm, but what will you do in return?",
      "choice_score": "bad",
      "choice_1": {
        "choice_description": "Vow to become her devout follower.",
        "god_message": "Devotion is pleasing, yet I must weigh your offer.",
        "choice_score": "good"
      },
      "choice_2": {
        "choice_description": "Propose to spread her teachings on love.",
        "god_message": "Teachings are valuable, but I need time to contemplate.",
        "choice_score": "neutral"
      },
      "choice_3": {
        "choice_description": "Promise to forsake all other gods for her.",
        "god_message": "Such exclusivity is rare, yet risky. I will consider.",
        "choice_score": "bad"
      }
    },
    "choice_3": {
      "choice_description": "Confess your own feelings of unworthiness in love.",
      "god_message": "Honesty is rare, but what do you seek from me?",
      "choice_score": "good",
      "choice_1": {
        "choice_description": "Ask for her guidance to improve yourself.",
        "god_message": "A quest for self-improvement? Intriguing. I shall ponder your request.",
        "choice_score": "good"
      },
      "choice_2": {
        "choice_description": "Request a potion to win over your beloved.",
        "god_message": "Magic is a tricky path. I need time to think on this.",
        "choice_score": "neutral"
      },
      "choice_3": {
        "choice_description": "Beg for her to intervene directly.",
        "god_message": "Direct intervention is not my usual way. I will contemplate.",
        "choice_score": "bad"
      }
    }
  },
  "choice_3": {
    "choice_description": "Inquire about her stance in the war of the gods.",
    "god_message": "The squabbles of deities are complex. Why do you ask?",
    "choice_score": "bad",
    "choice_1": {
      "choice_description": "Express your belief in peace and love.",
      "god_message": "A noble sentiment, but I must consider how it aligns with my desires.",
      "choice_score": "good",
      "choice_1": {
        "choice_description": "Offer to be an ambassador of peace in her name.",
        "god_message": "An ambassador for peace? A thoughtful offer. I shall think on it.",
        "choice_score": "good"
      },
      "choice_2": {
        "choice_description": "Suggest a truce between the warring gods.",
        "god_message": "Truces are temporary. I need time to decide.",
        "choice_score": "neutral"
      },
      "choice_3": {
        "choice_description": "Propose an alliance with her against other gods.",
        "god_message": "Alliances in war are delicate. I will ponder your proposition.",
        "choice_score": "bad"
      }
    },
    "choice_2": {
      "choice_description": "Pledge loyalty to her in the divine conflict.",
      "god_message": "Loyalty is valuable, yet what is your true intention?",
      "choice_score": "neutral",
      "choice_1": {
        "choice_description": "Offer to influence other mortals to support her.",
        "god_message": "Influence among mortals is intriguing. I will consider your offer.",
        "choice_score": "good"
      },
      "choice_2": {
        "choice_description": "Promise to seek vengeance against her enemies.",
        "god_message": "Vengeance is a dangerous path. I must contemplate this.",
        "choice_score": "neutral"
      },
      "choice_3": {
        "choice_description": "Swear to defeat her foes in battle.",
        "god_message": "Battle is a crude solution. I need time to think on this.",
        "choice_score": "bad"
      }
    },
    "choice_3": {
      "choice_description": "Question her about the benefits of joining the war.",
      "god_message": "You seek to understand the workings of the divine. A bold move.",
      "choice_score": "good",
      "choice_1": {
        "choice_description": "Argue that her involvement could turn the tide of war.",
        "god_message": "Turning the tide of war is a significant claim. I will consider it.",
        "choice_score": "good"
      },
      "choice_2": {
        "choice_description": "Suggest that staying out of the conflict is safest.",
        "god_message": "Safety is an illusion. I must ponder your words.",
        "choice_score": "neutral"
      },
      "choice_3": {
        "choice_description": "Insist that she must act to maintain her power.",
        "god_message": "Power is not gained by mere action alone. I need time to think.",
        "choice_score": "bad"
      }
    }
  }
}

class AphroTalker:
    instance=None
    def __init__(self) -> None:
        self.aphro=aphro
        pass
    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = AphroTalker()
        return cls.instance
    
    async def get_intro(self):
        aphro = self.aphro
        return JSONResponse(status_code=200, content={"message": aphro["god_message"], "choice_1": aphro["choice_1"]["choice_description"], "choice_2": aphro["choice_2"]["choice_description"], "choice_3": aphro["choice_3"]["choice_description"]})
    
    async def talk(self, choiceList):
        # choice list is list of chocies chosen so far
        # return list of choices following it
        aphro = self.aphro
        for i in choiceList:
            aphro = aphro[i]
        if len(choiceList)<=2:
            choices={"choice_1": aphro["choice_1"]["choice_description"], "choice_2": aphro["choice_2"]["choice_description"], "choice_3": aphro["choice_3"]["choice_description"]}
        return JSONResponse(status_code=200, content={"message": aphro["god_message"],'choices':choices,'score':aphro.get('choice_score',0)})
    


